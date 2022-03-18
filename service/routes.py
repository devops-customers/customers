"""
My Service

Describe what your service does here
"""

import os
import sys
import logging
from werkzeug.exceptions import NotFound
from flask import Flask, jsonify, request, url_for, make_response, abort
from . import status  # HTTP Status Codes

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Customer, DataValidationError

# Import Flask application
from . import app

######################################################################
# GET INDEX
######################################################################


@app.route("/")
def index():
    """Returns information about the service"""
    app.logger.info("Request for Base URL")
    return (
        jsonify(
            message="Customer Service",
            version="1.0.0",
            url=url_for("list_customers", _external=True),
        ),
        status.HTTP_200_OK,
    )

######################################################################
# RETRIEVE A CUSTOMER
######################################################################


@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customers(customer_id):
    """
 #   Retrieve a single Customer
 #   This endpoint will return a Customer based on it's id
 #   """
    app.logger.info("Request for customer with id: %s", customer_id)
    customer = Customer.find(customer_id)
    if not customer:
        raise NotFound(
            "customer with id '{}' was not found.".format(customer_id))

    app.logger.info("Returning customer: %s", customer.first_name)
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)

############################################################
#                 R E S T   A P I
############################################################


# -----------------------------------------------------------
# List customers
# -----------------------------------------------------------
@app.route("/customers", methods=[""])
def list_customers():
    return ""

# -----------------------------------------------------------
# Create customer
# -----------------------------------------------------------


@app.route("/customers", methods=["POST"])
def create_customer():
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
    location_url = url_for(
        "get_customers", customer_id=customer.id, _external=True)
    app.logger.info("Customer with ID [%s] created", customer.id)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

# -----------------------------------------------------------
# Delete customer
# -----------------------------------------------------------


@app.route("/", methods=[""])
def delete_customer(name):
    return ""


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    Customer.init_db(app)

# UPDATE AN EXISTING CUSTOMER
######################################################################


@app.route("/customers/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
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
