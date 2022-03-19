# Copyright 2016, 2021 John Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Models for Customer Service

All of the models are stored in this module

Models
------
Customer - A customer

Attributes:
-----------
first name
last name
email
phone number
"""
import logging
from enum import Enum
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


def init_db(app):
    """Initialize the SQLAlchemy app"""
    Customer.init_db(app)


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class Customer(db.Model):
    """ 
    Class that represents a Customer
    """

    ##################################################
    # Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    phone_number = db.Column(
        db.String(32), nullable=True)  # phone # is optional

    ##################################################
    # INSTANCE METHODS
    ##################################################

    def __repr__(self):
        return "<Customer %r id=[%s]>" % (self.last_name, self.id)

    def create(self):
        """ 
        Creates a Customer to the database
        """
        logger.info("Creating %s %s", self.first_name, self.last_name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def save(self):
        """ 
        Updates a Customer to the database
        """
        logger.info("Saving %s %s", self.first_name, self.last_name)
        db.session.commit()

    def update(self):
        """ 
        Updates a Customer to the database
        """
        logger.info("Saving %s", self.last_name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """ 
        Removes a Customer from the data store 
        """
        logger.info("Deleting %s", self.last_name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self) -> dict:
        """ Serializes a Customer into a dictionary """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone_number": self.phone_number
        }

    def deserialize(self, data: dict):
        """ 
        Deserializes a Customer from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.first_name = data["first_name"]
            self.last_name = data["last_name"]
            self.email = data["email"]
            self.phone_number = data.get("phone_number")
        except KeyError as error:
            raise DataValidationError(
                "Invalid Customer: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Customer body of request contained bad or no data"
            )
        return self
    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def init_db(cls, app: Flask):
        """Initializes the database session

        :param app: the Flask app
        :type data: Flask

        """
        logger.info("Initializing database")
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls) -> list:
        """Returns all of the Customers in the database"""
        logger.info("Processing all Customers")
        return cls.query.all()

    @classmethod
    def find(cls, customer_id: int):
        """ Finds a Customers by it's ID

        :param customer_id: the ID of the Customer to find
        :type customer_id: int

        :return: an instance with the customer_id or None if not found
        :rtype: Customer

        """
        logger.info("Processing lookup for id %s ...", customer_id)
        return cls.query.get(customer_id)

    @classmethod
    def find_or_404(cls, customer_id: int):
        """ Find a Customer by it's ID

        :param customer_id: the id of the Customer to find
        :type customer_id: int

        :return: an instance with the customer_id or 404_NOT_FOUND if not fonud
        :rtype: Customer

        """
        logger.info("Processing lookup or 404 for id %s ...", customer_id)
        return cls.query.get_or_404(customer_id)

    @classmethod
    def find_by_last_name(cls, last_name: str) -> list:
        """ Returns all Customers with the given last name

        :param last_name: the last name of the Customers you want to match
        :type last_name: str

        :return: a collection of Customers with that last name
        :rtype: list

        """
        logger.info("Processing last name query for %s ...", last_name)
        return cls.query.filter(cls.last_name == last_name)

    @classmethod
    def find_by_first_name(cls, first_name: str) -> list:
        """ Returns all Customers with the given first name

        :param first_name: the first name of the Customers you want to match
        :type first_name: str

        :return: a collection of Customers with that first name
        :rtype: list

        """
        logger.info("Processing first name query for %s ...", first_name)
        return cls.query.filter(cls.first_name == first_name)
