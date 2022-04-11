# Customer REST API for NYU DevOps

[![Build Status](https://github.com/jm9498/customers/actions/workflows/tdd.yml/badge.svg)](https://github.com/jm9498/customers/actions)
[![codecov](https://codecov.io/gh/devops-customers/customers/branch/main/graph/badge.svg?token=W0KHFZOJ4B)](https://codecov.io/gh/devops-customers/customers)

## Structure of Customers App

### Docker container files

**devcontainer.json** - Describes how VS Code should start the container and what to do after it connects. Building a Python 3 & PostgreSQL container with a number of extensions such as [pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) and [cucumber](https://cucumber.io/docs/installation/python/)

**Dockerfile** - Used to make and persist changes to the dev container, such as the installation of new software.
First it creates an image for a Python 3 development environment.
Then it is adding additional tools that are needed beyond Python 3.9 including sudo, vim, git, etc.
Then it creates a user for development purposes and gives that user passwordless sudo privileges.
Then it adds libraries for PostgreSQL
Then it creates a `PORT` variable and assigns it to port 8080.

**docker-compose.yml** - Allows you to bring up multiple containers. Also allows you to provision a database or message broker or any other service you need to develop with.

### Data model files

****init**.py** - Creates and configures the Flask app and sets up the logging and SQL database.

**error_handlers.py** - Creates methods for handling errors such as data validation errors, 400 bad request, and 404 not found errors, etc.

**models.py** - Defines the data model for the customers application. Uses a persistent base model with create, save, update, and delete functions. Also contains two data models, one for the main customers API and the second for the subordinate addresses API.
Also provides methods for querying the database models such as find by name, find by last name, find by first name, find by email, find by phone number, find by street, find by postal code.  

#### Customer model

| Label          | Name           | Type       | Nullable |
|----------------|----------------|------------|----------|
| Customer ID    | id             | Integer    | False    |
| Username       | name           | String(64) | False    |
| First Name     | first_name     | String(64) | False    |
| Last Name      | last_name      | String(64) | False    |
| Email          | email          | String(64) | False    |
| Phone Number   | phone_number   | String(32) | True     |
| Account Status | account_status | String(64) | False    |

#### Address model

| Label          | Name           | Type       | Nullable |
|----------------|----------------|------------|----------|
| Address ID     | id             | Integer    | False    |
| Customer ID    | customer_id    | Integer    | False    |
| Name           | name           | String(64) | False    |
| Street         | street         | String(64) | False    |
| City           | city           | String(64) | False    |
| State          | state          | String(2)  | False    |
| Postal Code    | postalcode     | String(64) | False    |

### API files

**routes.py** - Defines the REST API routes for the customer and address models. Below are the RESTful routes for `customers` and `addresses`

```bash
Endpoint          Methods  Rule
----------------  -------  -----------------------------------------------------
index             GET      /
list_customers    GET      /customers
get_customers     GET      /customers/<int:customer_id>
create_customers  POST     /customers
update_customers  PUT      /customers/<int:customer_id>
delete_customers  DELETE   /customers/<int:customer_id>

list_addresses    GET      /customers/<int:customer_id>/addresses
create_addresses  POST     /customers/<int:customer_id>/addresses
get_addresses     GET      /customers/<int:customer_id>/addresses/<int:address_id>
update_addresses  PUT      /customers/<int:customer_id>/addresses/<int:address_id>
delete_addresses  DELETE   /customers/<int:customer_id>/addresses/<int:address_id>
```

The action endpoints for `customers` are below:

```bash
Endpoint          Methods  Rule
----------------  -------  -----------------------------------------------------
suspend_customers PUT      /customers/<int:customer_id>/suspend
restore_customers PUT      /customers/<int:customer_id>/restore
```

**status.py** - Includes a set of descriptive HTTP status codes to make code more readable.

### Testing files

**factories.py** - factories to generate fake data for testing data models and services.

**test_models.py** - test cases for the customers and addresses data models

**test_routes.py** - test cases for the customers and addresses services

### Cloud app files

**Procfile** - Contains the command to run when your application starts on IBM Cloud. It is represented in the form `web: <command>` where `<command>` in this sample case is to run the `gunicorn` command and passing in the location of the Flask app as `service:app`.

**requirements.txt** - - Contains the external python packages that are required by the application. These will be downloaded from the [python package index](https://pypi.python.org/pypi/) and installed via the python package installer (pip) during the buildpack's compile stage when you execute the cf push command. In this sample case we wish to download the [Flask package](https://pypi.python.org/pypi/Flask) at version 2.0.2

**runtime.txt** - Controls which python runtime to use. In this case we want to use Python 3.9.

**manifest.yml** - Controls how the app will be deployed in IBM Cloud and specifies memory and other services that are needed to be bound to it.

## Reference for DevOps commands

### Run the flask app locally

To run the service, use the below command

```bash
flask run -h 0.0.0.0 -p 8000
```

You must pass the parameters `-h 0.0.0.0` to have it listed on all network adapters so that the nextwork port `8000` can be forwarded by `docker` to your host computer so that you can open the web page in a local browser at: <http://localhost:8000>

### Run flask app in browser using honcho

You can run the code to test it out in your browser with the following command:

```bash
honcho start
```

You should be able to see it at <http://localhost:8080/>
When you are done, you can use `Ctrl+c` to stop the server

### IBM Cloud commands

#### Login

Login to IBM Cloud and set the api endpoint to the IBM Cloud region you wish to deploy to:

```bash
ibmcloud cf login -a https://cloud.ibm.com
```

The login will ask you for your `email` (username) and `password`, plus the `organization` and `space` if there is more than one to choose from
You can also log in using the api key with the following command:

```bash
ibmcloud login --apikey @~/.bluemix/apikey.json -r us-south
```

#### Target Cloud Foundry

We need to target Cloud Foundry as our environment. So we will use the following command to target:

```bash
ibmcloud target -o ORG -s SPACE
```

Where `ORG` is your cloud foundry org and `SPACE` is your cloud foundry space
As an example:

```bash
ibmcloud target -o llb6986@nyu.edu -s dev
```

#### List resources

You can use the Cloud Foundry CLI to list apps and services

```bash
ibmcloud cf apps
```

```bash
ibmcloud cf services
```

#### Push to cloud

From the root directory of the application code, execute the following to deploy the application to IBM Cloud. (By default the `route` (application URL) will be based on your application name

```bash
ibmcloud cf push
