"""
Customer Service

Paths:
------
GET /customers - Returns a list all of the Customers
GET /customers/{id} - Returns the Customer with a given id number
POST /customers - creates a new Customer record in the database
PUT /customers/{id} - updates a Customer record in the database
DELETE /customers/{id} - deletes a Customer record in the database
"""

from flask import Flask, jsonify, request, url_for, make_response, abort
from werkzeug.exceptions import NotFound
from service.models import Customer, DataValidationError
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
    app.logger.info("Request for pet list")
    customers = []
    email = request.args.get("email")
    last_name = request.args.get("last_name")
    if email:
        customers = Customer.find_by_email(email)
    elif last_name:
        customers = Customer.find_by_last_name(last_name)
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
@app.route("/customers", methods=[""])
def delete_customer(name):
    return ""

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
