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
from werkzeug.exceptions import NotFound
from service.models import Customer, Address, DataValidationError
from . import status  # HTTP Status Codes
from . import app # Import Flask application

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    app.logger.info("Request for Root URL")
    return (
        jsonify(
            name="Customer Service",
            version="1.0",
            url=url_for("list_customers", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
# LIST ALL CUSTOMERS
######################################################################
@app.route("/customers", methods=["GET"])
def list_customers():
    """Returns all of the Customers"""
    app.logger.info("Request for Customer list")
    customers = []
    email = request.args.get("email")
    last_name = request.args.get("last_name")
    name = request.args.get("name")
    phone_number = request.args.get("phone_number")
    if email:
        customers = Customer.find_by_email(email)
    elif last_name:
        customers = Customer.find_by_last_name(last_name)
    elif name:
        customers =Customer.find_by_name(name)
    elif phone_number:
        customers =Customer.find_by_phone_number(phone_number)
    else:
        customers = Customer.all()

    results = [customer.serialize() for customer in customers]
    app.logger.info("Returning %d customers", len(results))
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# RETRIEVE A CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customers(customer_id):
    """
    Retrieve a single Customer

    This endpoint will return a Customer based on it's id
    """
    app.logger.info("Request for customer with id: %s", customer_id)
    customer = Customer.find(customer_id)
    if not customer:
        raise NotFound("customer with id '{}' was not found.".format(customer_id))

    app.logger.info("Returning customer: %s %s", customer.first_name, customer.last_name)
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)

######################################################################
# CREATE A NEW CUSTOMER
######################################################################
@app.route("/customers", methods=["POST"])
def create_customers():
    """
    Creates a Customer Account
    This endpoint will create a Customer Account based on the data in the body that is posted
    """
    app.logger.info("Request to create a Customer Account")
    check_content_type("application/json")
    customer = Customer()
    customer.deserialize(request.get_json())
    customer.create()
    message = customer.serialize()
    location_url = url_for("get_customers", customer_id=customer.id, _external=True)
    
    app.logger.info("Customer with ID [%s] created", customer.id)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# UPDATE AN EXISTING CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>", methods=["PUT"])
def update_customers(customer_id):
    """Update a Customer

    This endpoint will update a Customer based the body that is posted
    """
    app.logger.info("Request to update customer with id: %s", customer_id)
    check_content_type("application/json")
    customer = Customer.find(customer_id)
    if not customer:
        raise NotFound(
           "Customer with id '{}' was not found.".format(customer_id))
    customer.deserialize(request.get_json())
    customer.id = customer_id
    customer.update()

    app.logger.info("Customerwith ID [%s] updated.", customer.id)
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE A CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customers(customer_id):
    """
    Delete a Customer

    This endpoint will delete a Customer based the id specified in the path
    """
    app.logger.info("Request to delete customer with id: %s", customer_id)
    customer = Customer.find(customer_id)
    if customer:
        customer.delete()

    app.logger.info("Customer with ID [%s] delete complete.", customer_id)
    return make_response("", status.HTTP_204_NO_CONTENT)

#---------------------------------------------------------------------
#                A D D R E S S   M E T H O D S
#---------------------------------------------------------------------
######################################################################
# LIST ADDRESSES
######################################################################
@app.route("/customers/<int:customer_id>/addresses", methods=["GET"])
def list_addresses(customer_id):
    """ Returns all of the Addresses for an Customer """
    app.logger.info("Request for all Addresses for Customer with id: %s", customer_id)

    customer = Customer.find(customer_id)
    if not customer:
        abort(status.HTTP_404_NOT_FOUND, f"Customer with id '{customer_id}' could not be found.")
    
    results = [address.serialize() for address in customer.addresses]
    return make_response(jsonify(results), status.HTTP_200_OK)

######################################################################
# ADD AN ADDRESS TO A CUSTOMER
######################################################################
@app.route('/customers/<int:customer_id>/addresses', methods=["POST"])
def create_addresses(customer_id):
    """ 
    Create an Address on a Customer
    
    This endpoint will add an address to an customer
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
    return make_response(jsonify(message), status.HTTP_201_CREATED)

######################################################################
# RETRIEVE AN ADDRESS FROM CUSTOMER
######################################################################
@app.route('/customers/<int:customer_id>/addresses/<int:address_id>', methods=['GET'])
def get_addresses(customer_id, address_id):
    """
    Get an Address
    
    This endpoint returns just an address
    """ 
    app.logger.info("Request to retrieve address %s for Customer id: %s", (address_id, customer_id))

    address = Address.find(address_id)
    if not address:
        abort(status.HTTP_404_NOT_FOUND, f"Customer with Address id '{address_id}' could not be found.")
    
    return make_response(jsonify(address.serialize()), status.HTTP_200_OK)

######################################################################
# UPDATE AN ADDRESS
######################################################################
@app.route("/customers/<int:customer_id>/addresses/<int:address_id>", methods=['PUT'])
def update_addresses(customer_id, address_id):
    """ 
    Update an Address
    
    This endpoint will update an Address based on the body that is posted
    """
    app.logger.info("Request to update Address %s for Customer id: %s", (address_id, customer_id))
    check_content_type("application/json")
    address = Address.find(address_id)
    if not address:
        abort(status.HTTP_404_NOT_FOUND, f"Customer with Address id '{address_id}' could not be found.")
    
    address.deserialize(request.get_json())
    address.id = address_id
    address.update()
    return make_response(jsonify(address.serialize()), status.HTTP_200_OK)
    

######################################################################
# DELETE AN ADDRESS
######################################################################
@app.route("/customers/<int:customer_id>/addresses/<int:address_id>", methods=['DELETE'])
def delete_addresses(customer_id, address_id):
    """ 
    Delete an Address
    
    This endpoint will delete an Address based on the id specified in the path
    """
    app.logger.info("Request to delete Address %s for Customer id: %s", (address_id, customer_id))

    address = Address.find(address_id)
    if address:
        address.delete()

    return make_response("", status.HTTP_204_NO_CONTENT)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Content-Type must be {}".format(media_type),
    )

######################################################################
# UPDATE AN CUSTOMER'S STATUS to SUSPEND
######################################################################
@app.route("/customers/<int:customer_id>/suspend", methods=["PUT"])
def suspend_customers(customer_id):
    """Update a Customer's status to suspend

    This endpoint will update a Customer based the body that is posted
    """
    app.logger.info("Request to suspend customer with id: %s", customer_id)
    check_content_type("application/json")
    customer = Customer.find(customer_id)
    if not customer:
        raise NotFound(
           "Customer with id '{}' was not found.".format(customer_id))
    customer.deserialize(request.get_json())
    customer.account_status = "suspended"
    customer.update()

    app.logger.info("Customerwith ID [%s] updated.", customer.id)
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)

######################################################################
# RESTORE A SUSPENDED CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>/restore", methods=["PUT"])
def restore_customers(customer_id):
    """ Update a customer's status from suspend to active
    
    This endpoint will update a customer based on the body that is posted
    """
    app.logger.info("Request to restore customer with id: %s", customer_id)
    check_content_type("application/json")
    customer = Customer.find(customer_id)
    if not customer:
        raise NotFound(
            "Customer with id '{}' was not found.".format(customer_id)
        )
    customer.deserialize(request.get_json())
    customer.account_status = "active"
    customer.update()

    app.logger.info("Customer with ID [%s] updated.", customer.id)
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)

