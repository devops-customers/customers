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
from service.models import YourResourceModel, DataValidationError

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


############################################################
#                 R E S T   A P I
############################################################


#-----------------------------------------------------------
# List customers
#-----------------------------------------------------------
@app.route("/customers", methods=["GET"])
def list_customers():
    """Lists all of the customers in the database
    Returns:
        list: an array of customer names
    """
    app.logger.info("Request to list all customers...")

    # Get the database key names as a list
    names = customer.keys("*")
    return jsonify(names)


#-----------------------------------------------------------
# Create customers
#-----------------------------------------------------------
@app.route("/customers/<name>", methods=["POST"])
def create_customers(name):
    """Creates a new customer and stores it in the database
    Args:
        name (str): the name of the customer to create
    Returns:
        dict: the customer and it's value
    """
    app.logger.info(f"Request to Create customer {name}...")

    # See if the customer already exists and send an error if it does
    count = customer.get(name)
    if count is not None:
        abort(HTTP_409_CONFLICT, f"customer {name} already exists")

    # Create the new customer and set it to zero
    customer.set(name, 0)

    # Set the location header and return the new customer
    location_url = url_for("read_customers", name=name, _external=True)
    return (
        jsonify(name=name, customer=0),
        HTTP_201_CREATED,
        {"Location": location_url},
    )


#-----------------------------------------------------------
# Read customers
#-----------------------------------------------------------
@app.route("/customers/<name>", methods=["GET"])
def read_customers(name):
    """Reads a customer from the database
    Args:
        name (str): the name of the customer to read
    Returns:
        dict: the customer and it's value
    """
    app.logger.info(f"Request to Read customer {name}...")

    # Get the current customer
    count = customer.get(name)

    # Send an error if it does not exist
    if count is None:
        abort(HTTP_404_NOT_FOUND, f"customer {name} does not exist")

    # Return the customer
    return jsonify(name=name, customer=int(count))


#-----------------------------------------------------------
# Update customers
#-----------------------------------------------------------
@app.route("/customers/<name>", methods=["PUT"])
def update_customers(name):
    """Updates a ciunter in the database
    Args:
        name (str): the name of the customer to update
    Returns:
        dict: the customer and it's value
    """
    app.logger.info(f"Request to Update customer {name}...")

    # Get the current customer
    count = customer.get(name)

    # Send an error if it does not exist
    if count is None:
        abort(HTTP_404_NOT_FOUND, f"customer {name} does not exist")

    # Increment the customer and return the new value
    count = customer.incr(name)
    return jsonify(name=name, customer=count)


#-----------------------------------------------------------
# Delete customers
#-----------------------------------------------------------
@app.route("/customers/<name>", methods=["DELETE"])
def delete_customers(name):
    """Delete a customer from the database
    Args:
        name (str): the name of the customer to delete
    Returns:
        str: always returns an empty string
    """
    app.logger.info(f"Request to Delete customer {name}...")

    # Get the current customer
    count = customer.get(name)

    # If it exists delete it, if not do nothing
    if count is not None:
        customer.delete(name)

    # Delete always returns 204
    return "", HTTP_204_NO_CONTENT



######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    YourResourceModel.init_db(app)
