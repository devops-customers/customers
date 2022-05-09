# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Customer Service
Paths:
------
GET /customers - Returns a list all of the Customers
GET /customers/{id} - Returns the Customer with a given id number
POST /customers - creates a new Customer record in the database
PUT /customers/{id} - updates a Customer record in the database
DELETE /customers/{id} - deletes a Customer record in the database
GET /customers/{id}/addresses - Returns a list of all the addresses for a customer
POST /customers/{id}/addresses - Add an address to a customer
GET /customers/{id}/addresses/{id} - Get a specific address for a given customer
PUT /customers/{id}/addresses/{id} - Update a specific address for a given customer
DELETE /customers/{id}/addresses/{id} - Delete a specific address for a given customer
Actions:
--------
PUT /customers/{id}/suspend - suspend a customer account
PUT /customers/{id}/restore - restore a suspended customer account
"""
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_restx import Api, Resource, fields, reqparse, inputs
from service.models import Customer, Address, DataValidationError, DatabaseConnectionError
from . import app, status 

######################################################################
# Configure the Root route before OpenAPI
######################################################################
@app.route("/")
def index():
    """Base URL for our service"""
    return app.send_static_file("index.html")

######################################################################
# CREATE PAGE FOR ADDRESS UI
######################################################################
@app.route("/address")
def address():
    return app.send_static_file("address.html")

######################################################################
# Configure Swagger before initializing it
######################################################################
api = Api(app,
          version='1.0.0',
          title='Customer REST API Service',
          description='This is a sample server Customer server.',
          default='customers',
          default_label='Customer operations',
          doc='/apidocs', # default also could use doc='/apidocs/'
         )

#Define the model so the docs reflect what can be sent
create_model = api.model('Customer', {
    'name': fields.String(required=True, description='The username of the Customer'),
    'first_name': fields.String(required=True, description='The first name of the Customer'),
    'last_name': fields.String(required=True, description='The last name of the Customer'),
    'email': fields.String(required=True, description='The email address of the Customer'),
    'phone_number': fields.String(required=True, description='The phone number of the Customer'),
    'account_status': fields.String(required=True, description='The status of the Customer account')
})

customer_model = api.inherit('CustomerModel', create_model, {
    'id': fields.Integer(readOnly=True, description='The unique id assigned internally by service'),
    'addresses': fields.List(cls_or_instance=fields.Raw, description='collection of all addresses associated with the Customer')
})

create_address_model = api.model('Address', {
    'customer_id': fields.Integer(required=True, description='The customer id the Address is associated with'),
    'name': fields.String(required=True, description='The name of the Address'),
    'street': fields.String(required=True, description='The street piece of the Address'),
    'city': fields.String(required=True, description='The city for the Address'),
    'state': fields.String(required=True, description='The state abbreviation for the Address'),
    'postalcode': fields.String(required=True, description='The postal code for the Address')
})

address_model = api.inherit('AddressModel', create_address_model, {
    'id': fields.Integer(readOnly=True, description='The unique id assigned internally by service')
})

######################################################################
# Add all list functions
######################################################################
customer_args = reqparse.RequestParser()
customer_args.add_argument('name', type=str, location='args', required=False, help='List Customer by Username')
customer_args.add_argument('first_name', type=str, location='args', required=False, help='List Customer by First Name')
customer_args.add_argument('last_name', type=str, location='args', required=False, help='List Customer by Last Name')
customer_args.add_argument('email', type=str, location='args', required=False, help='List Customer by Email')
customer_args.add_argument('phone_number', type=str, location='args', required=False, help='List Customer by Phone Number')
customer_args.add_argument('postalcode', type=str, location='args', required=False, help='List Customer by Postal Code')
customer_args.add_argument('street', type=str, location='args', required=False, help='List Customer by Street Address')

######################################################################
# Special Error Handlers
######################################################################
@api.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    message = str(error)
    app.logger.error(message)
    return {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'error': 'Bad Request',
        'message': message
    }, status.HTTP_400_BAD_REQUEST

@api.errorhandler(DatabaseConnectionError)
def database_connection_error(error):
    """ Handles Database Errors from connection attempts """
    message = str(error)
    app.logger.critical(message)
    return {
        'status_code': status.HTTP_503_SERVICE_UNAVAILABLE,
        'error': 'Service Unavailable',
        'message': message
    }, status.HTTP_503_SERVICE_UNAVAILABLE

######################################################################
#  PATH: /customers/{id}
######################################################################
@api.route('/customers/<customer_id>')
@api.param('customer_id', 'The Customer identifier')
class CustomerResource(Resource):
    """ 
    CustomerResource class

    Allows the manipulation of a single Customer
    GET /customer{id} - Returns a Customer with the id
    PUT /customer{is} - Update a Customer with the id
    DELETE /customer{id} - Deletes a Customer with the id
    """
    # ------------------------------------------------------------------
    # RETRIEVE A CUSTOMER
    # ------------------------------------------------------------------
    @api.doc('get_customers')
    @api.response(404, 'Customer not found')
    @api.marshal_with(customer_model)
    def get(self, customer_id):
        """ 
        Retrieve a single Customer
        
        This endpoint will return a Customer based on its id
        """
        app.logger.info("Request for customer with id: %s", customer_id)
        customer = Customer.find(customer_id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, "Customer with id '{}' was not found.".format(customer_id))
        app.logger.info("Returning customer: %s", customer.id)
        return customer.serialize(), status.HTTP_200_OK
    
    # ------------------------------------------------------------------
    # UPDATE AN EXISTING CUSTOMER
    # ------------------------------------------------------------------
    @api.doc('update_customers')
    @api.response(404, 'Customer not found')
    @api.response(400, 'The posted Customer data was not valid')
    @api.expect(customer_model)
    @api.marshal_with(customer_model)
    def put(self, customer_id):
        """ 
        Update a CUstomer

        This endpoint will update a Customer based on the body that is posted
        """
        app.logger.info("Request to update Customer with id: %s", customer_id)
        check_content_type("application/json")
        customer = Customer.find(customer_id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, "Customer with id '{}' was not found.".format(customer_id))
        
        app.logger.debug('Payload = %s', api.payload)
        data = api.payload
        customer.deserialize(data)
        customer.id = customer_id
        customer.update()
        app.logger.info("Customer with id [%s] updated.", customer.id)
        return customer.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE A CUSTOMER
    # ------------------------------------------------------------------
    @api.doc('delete_customers')
    @api.response(204, 'Customer deleted')
    def delete(self, customer_id):
        """ 
        Delete a Customer
        
        This endpoint will delete a Customer based on the id specified in the path 
        """
        app.logger.info("Request to delete customer with id: %s", customer_id)

        customer = Customer.find(customer_id)
        if customer:
            customer.delete()

        app.logger.info("Customer with id [%s] deleted successfully.", customer_id)
        return '', status.HTTP_204_NO_CONTENT

######################################################################
#  PATH: /customers
######################################################################
@api.route('/customers', strict_slashes=False)
class CustomerCollection(Resource):
    """ Handles all interactions with collections of Customers """

    # ------------------------------------------------------------------
    # LIST ALL CUSTOMERS
    # ------------------------------------------------------------------
    @api.doc('list_customers')
    @api.expect(customer_args, validate=True)
    @api.marshal_list_with(customer_model)
    def get(self):
        """ Returns all of the Customers """
        app.logger.info("Request for Customer List")

        customers = []
        name = request.args.get("name")
        first_name = request.args.get("first_name")
        last_name = request.args.get("last_name")
        email = request.args.get("email")
        phone_number = request.args.get("phone_number")
        postalcode = request.args.get("postalcode")
        street = request.args.get("street")

        if name:
            customers = Customer.find_by_name(name)
        elif first_name:
            customers = Customer.find_by_first_name(first_name)
        elif last_name:
            customers = Customer.find_by_last_name(last_name)
        elif email:
            customers = Customer.find_by_email(email)
        elif phone_number:
            customers = Customer.find_by_phone_number(phone_number)
        elif postalcode:
            customers = Customer.find_by_postalcode(postalcode)
        elif street:
            customers = Customer.find_by_street(street)
        else:
            customers = Customer.all()
        
        results = [customer.serialize() for customer in customers]
        app.logger.info("Request %d customers", len(results))
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW CUSTOMER
    # ------------------------------------------------------------------
    @api.doc('create_customers')
    @api.response(400, 'The posted data was not valid')
    @api.expect(create_model)
    @api.marshal_with(customer_model, code=201)
    def post(self):
        """ 
        Create a Customer 
        This endpoint will create a Customer based on the data in the body that is posted
        """
        app.logger.info("Request to create a Customer")
        check_content_type("application/json")
        customer = Customer()
        app.logger.debug('Payload = %s', api.payload)
        customer.deserialize(request.get_json())
        customer.create()
        app.logger.info("Customer with id [%s] created.", customer.id)
        location_url = api.url_for(CustomerResource, customer_id = customer.id, _external=True)
        return customer.serialize(), status.HTTP_201_CREATED, {"Location": location_url}

######################################################################
#  PATH: /customers/{id}/suspend
######################################################################
@api.route('/customers/<int:customer_id>/suspend')
@api.param('customer_id', 'The Customer identifier')
class SuspendResource(Resource):
    """ Suspend actions on a Customer """
    @api.doc('suspend_customers')
    @api.response(404, 'Customer not found')
    @api.response(409, 'The Customer is not available for suspension')
    def put(self, customer_id):
        """
        Suspending a Customer
        This endpoint will suspend a Customer based on customer_id
        """
        app.logger.info(f"Request to suspend customer with id {customer_id}")
        customer = Customer.find(customer_id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND,
                  "Customer with id '{}' was not found.".format(customer_id))
        customer.deserialize(api.payload)
        customer.account_status = "suspended"
        customer.update()
        app.logger.info("Customer with ID [%s] updated.", customer.id)
        return customer.serialize(), status.HTTP_200_OK

######################################################################
#  PATH: /customers/{id}/restore
######################################################################
@api.route("/customers/<int:customer_id>/restore")
@api.param('customer_id', 'The Customer identifier')
class RestoreResource(Resource):
    """ Restore actions on a Customer """
    @api.doc('restore_customers')
    @api.response(404, 'Customer not found')
    @api.response(409, 'The Customer is not available for restoration')
    def put(self, customer_id):
        """ 
        Restoring a customer 
        This endpoint will restore a customer based on customer_id
        """
        app.logger.info("Request to restore customer with id: %s", customer_id)
        check_content_type("application/json")
        customer = Customer.find(customer_id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, "Customer with id '{}' was not found.".format(customer_id))
        customer.deserialize(api.payload)
        customer.account_status = 'active'
        customer.update()

        app.logger.info("Customer with ID [%s] updated.", customer.id)
        return customer.serialize(), status.HTTP_200_OK

######################################################################
#  PATH: /customers/{customer_id}/addresses/{address_id}
######################################################################
@api.route('/customers/<int:customer_id>/addresses/<int:address_id>')
@api.param('address_id', 'The Address identifier')
@api.param('customer_id', 'The Customer identifier')
class CustomerAddressResource(Resource):
    """ 
    CustomerAddressResource class
    Allows the manipulation of a single Customer Address
    GET /customers/{customer_id}/addresses/{id} - Returns a Customer Address with the id
    PUT /customers/{customer_id}/addresses/{id} - Updates a Customer Address with the id
    DELETE /customers/{customer_id}/addresses/{id} - Deletes a Customer Address with the id
    """

    # ------------------------------------------------------------------
    # RETRIEVE AN ADDRESS
    # ------------------------------------------------------------------
    @api.doc('get_addresses')
    @api.response(404, 'Address not found')
    @api.marshal_with(address_model)
    def get(self, customer_id, address_id):
        """ 
        Get a Customer Address

        This endpoint will return an address based on its id and its customers's id
        """
        app.logger.info("Request to retrieve Customer Address %s for Customer id %s", (address_id, customer_id))
        address = Address.find(address_id)
        if not address:
            abort(status.HTTP_404_NOT_FOUND, f"Customer with id '{customer_id}' and address is '{address_id}' could not be found.")
        
        return address.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN ADDRESS
    # ------------------------------------------------------------------
    @api.doc('update_address')
    @api.response(404, 'Address not found')
    @api.response(400, 'The posted Address data was not valid')
    @api.expect(address_model)
    @api.marshal_with(address_model)
    def put(self, customer_id, address_id):
        """ 
        Update an Address
        
        This endpoint will update an Address based on the body that is posted
        """
        app.logger.info("Request to update Address %s for Customer id: %s", (address_id, customer_id))
        check_content_type("application/json")

        address = Address.find(address_id)
        if not address:
            abort(status.HTTP_404_NOT_FOUND, f"Customer with id '{customer_id}' and address '{address_id}' could not be found.")
        
        address.deserialize(api.payload)
        address.id = address_id
        address.update()
        return address.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE AN ADDRESS
    # ------------------------------------------------------------------
    @api.doc('delete_addresses')
    @api.response(204, 'Customer Address deleted')
    def delete(self, customer_id, address_id):
        """ 
        Delete an Address
        
        This endpoint will delete an Item based on the id specified in the path
        """
        app.logger.info("Request to delete Address %s for Customer id: %s", (address_id, customer_id))

        address = Address.find(address_id)
        if address:
            address.delete()

        return make_response("", status.HTTP_204_NO_CONTENT)

######################################################################
#  PATH: /customers/{customer_id}/addresses
######################################################################
@api.route('/customers/<int:customer_id>/addresses', strict_slashes=False)
@api.param('customer_id', 'The Customer identifier')
class CustomerAddressCollection(Resource):
    """ Handles all interactions with collections of Customer Addresses """

    # ------------------------------------------------------------------
    # LIST ALL ADDRESSES
    # ------------------------------------------------------------------
    @api.doc('list_addresses')
    @api.marshal_list_with(address_model)
    def get(self, customer_id):
        """ Returns all of the Addresses for a Customer """
        app.logger.info("Request for all Address for Customer with id: %s", customer_id)

        customer = Customer.find(customer_id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, f"Order with id '{customer_id}' could not be found.")

        results = [address.serialize() for address in customer.addresses]
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW ADDRESS
    # ------------------------------------------------------------------
    @api.doc('create_addresses')
    @api.response(400, 'The posted data was not valid')
    @api.expect(create_model)
    @api.marshal_with(address_model, code=201)
    def post(self, customer_id):
        """ 
        Create an Address on a Customer
        This endpoint will add an Address to a Customer
        """
        app.logger.info("Request to create an Address for Customer with id: %s", customer_id)
        check_content_type("application/json")

        customer = Customer.find(customer_id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, f"Customer with id '{customer_id}' could not be found.")

        address = Address()
        address.deserialize(request.get_json())
        customer.addresses.append(address)
        customer.update()
        message = address.serialize()
        return message, status.HTTP_201_CREATED
        

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def abort(error_code: int, message: str):
    """Logs errors before aborting"""
    app.logger.error(message)
    api.abort(error_code, message)

@app.before_first_request
def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    Customer.init_db(app)
    Address.init_db(app)

def check_content_type(content_type):
    """ Checks that the media type is correct """
    if request.headers["Content-Type"] == content_type:
        return
    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, f"Content-Type must be {content_type}")

# load sample data
def data_load(payload):
    """ Loads a Customer into the database """
    customer = Customer(payload['name'], payload['first_name'], payload['last_name'], payload['email'], payload['phone_number'], payload['account_status'], payload['addresses'])
    customer.create()

def data_reset():
    """ Removes all Customers from the database """
    Customer.remove_all()