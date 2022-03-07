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
@app.route("/customers", methods=[""])
def list_customers():
    

#-----------------------------------------------------------
# Create customer
#-----------------------------------------------------------
@app.route("", methods=[""])
def create_customer(name):
    


#-----------------------------------------------------------
# Read customer
#-----------------------------------------------------------
@app.route("", methods=[""])
def read_customer(name):
    

#-----------------------------------------------------------
# Update customer
#-----------------------------------------------------------
@app.route("", methods=[""])
def update_customer(name):
    

#-----------------------------------------------------------
# Delete customer
#-----------------------------------------------------------
@app.route("", methods=[""])
def delete_customer(name):
    


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    YourResourceModel.init_db(app)
