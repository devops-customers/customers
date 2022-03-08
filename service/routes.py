"""
My Service

Describe what your service does here
"""

import os
import sys
import logging
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
    return jsonify(
        status=HTTP_200_OK,
        message="Customer Service",
        version="1.0.0",
        url=url_for("list_customers", _external=True),
    )

######################################################################
# RETRIEVE A CUSTOMER
######################################################################
@app.route("/pets/<int:pet_id>", methods=["GET"])
def get_customers(customer_id):
    """
    Retrieve a single Customer
    This endpoint will return a Customer based on it's id
    """
    app.logger.info("Request for customer with id: %s", customer_id)
    customer = customer.find(customer_id)
    if not customer:
        raise NotFound("customer with id '{}' was not found.".format(customer_id))

    app.logger.info("Returning customer: %s", customer.name)
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)

############################################################
#                 R E S T   A P I
############################################################


#-----------------------------------------------------------
# List customers
#-----------------------------------------------------------
@app.route("/customers", methods=[""])
def list_customers():
    return ""

#-----------------------------------------------------------
# Create customer
#-----------------------------------------------------------
@app.route("", methods=[""])
def create_customer(name):
    return ""


#-----------------------------------------------------------
# Read customer
#-----------------------------------------------------------
@app.route("", methods=[""])
def read_customer(name):
    return ""
    

#-----------------------------------------------------------
# Update customer
#-----------------------------------------------------------
@app.route("", methods=[""])
def update_customer(name):
    return ""

#-----------------------------------------------------------
# Delete customer
#-----------------------------------------------------------
@app.route("", methods=[""])
def delete_customer(name):
    return ""


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    Customer.init_db(app)
