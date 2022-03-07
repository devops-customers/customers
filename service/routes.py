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
    """ Root URL response """
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    YourResourceModel.init_db(app)

# UPDATE AN EXISTING CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>", methods=["PUT"])
defupdate_customer(customer_id):
"""Update a Customer

    This endpoint will update a Customer based the body that is posted
    """
app.logger.info("Request to update customer with id: %s", customer_id)
check_content_type("application/json")
customer=customer.find(customer_id)
ifnotcustomer:
raiseNotFound("Customer with id '{}' was not found.".format(customer_id))
customer.deserialize(request.get_json())
customer.id=customer_id
customer.update()

app.logger.info("Customerwith ID [%s] updated.", customer.id)
returnmake_response(jsonify(customer.serialize()), status.HTTP_200_OK)
