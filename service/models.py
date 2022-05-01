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
import os
import logging
from retry import retry
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from requests import HTTPError, ConnectionError

logger = logging.getLogger("flask.app")

# global variables for retry (must be int)
RETRY_COUNT = int(os.environ.get("RETRY_COUNT", 10))
RETRY_DELAY = int(os.environ.get("RETRY_DELAY", 1))
RETRY_BACKOFF = int(os.environ.get("RETRY_BACKOFF", 2))

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

def init_db(app):
    """Initialize the SQLAlchemy app"""
    Customer.init_db(app)
    Address.init_db(app)

class DatabaseConnectionError(Exception):
    """ Custom exception when database connection fails"""

class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""
    pass

######################################################################
#  P E R S I S T E N T   B A S E   M O D E L
######################################################################
class PersistentBase():
    """ Base class added persistent methods """

    def create(self):
        """ 
        Creates a Customer to the database
        """
        logger.info("Creating %s", self.id)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """ 
        Updates a Customer to the database
        """
        logger.info("Saving %s", self.id)
        db.session.commit()

    def delete(self):
        """ 
        Removes an Account from the data store 
        """
        logger.info("Deleting %s", self.id)
        db.session.delete(self)
        db.session.commit()

    @classmethod
    @retry(
        HTTPError, 
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )
    def init_db(cls, app: Flask):
        """Initializes the database session

        :param app: the Flask app
        :type data: Flask

        """
        logger.info("Initializing database")
        # This is where we initialize SQLAlchemy from the Flask app
        cls.app = app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    @retry(
        HTTPError, 
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )
    def remove_all(cls):
        """ Removes all documents from the database (use for testing) """
        db.drop_all()

    @classmethod
    @retry(
        HTTPError, 
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )
    def all(cls) -> list:
        """Returns all of the Customers in the database"""
        logger.info("Processing all Records")
        return cls.query.all()

    @classmethod
    @retry(
        HTTPError, 
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )
    def find(cls, by_id: int):
        """ Finds a Record by it's ID

        :param customer_id: the ID of the Customer to find
        :type customer_id: int

        :return: an instance with the customer_id or None if not found
        :rtype: Customer

        """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    @retry(
        HTTPError, 
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )
    def find_or_404(cls, customer_id: int):
        """Find a Customer by it's id or 404
        
        :param id: the id of the Customer to find
        :type id: int

        :return: an instance with the id, or 404_NOT_FOUND if not found
        :rtype: Customer
        """
        logger.info("Processing lookup or 404 for id %s...", customer_id)
        return cls.query.get_or_404(customer_id)

######################################################################
#  A D D R E S S   M O D E L
######################################################################
class Address(db.Model, PersistentBase):
    """ 
    Class that represents Customer Addresses
    
    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """

    ##################################################
    # Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    name = db.Column(db.String(64)) # e.g., work, home, vacation, etc.
    street = db.Column(db.String(64))
    city = db.Column(db.String(64))
    state = db.Column(db.String(2))
    postalcode = db.Column(db.String(16))

    ##################################################
    # INSTANCE METHODS
    ##################################################
    def __repr__(self):
        return "<Address %r id=[%s] customer[%s]>" % (self.name, self.id, self.customer_id)

    def __str__(self):
        return "%s: %s, %s, %s %s" % (self.name, self.street, self.city, self.state, self.postalcode)

    def serialize(self):
        """ Serializes an Address into a dictionary """
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "name": self.name,
            "street": self.street,
            "city": self.city,
            "state": self.state,
            "postalcode": self.postalcode
        }
    
    def deserialize(self, data):
        """
        Deserializes an Address from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.customer_id = data["customer_id"]
            self.name = data["name"]
            self.street = data["street"]
            self.city = data["city"]
            self.state = data["state"]
            self.postalcode = data["postalcode"]
        except KeyError as error:
            raise DataValidationError("Invalid Address: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Address: body of request contained" "bad or no data"
            )
        return self

######################################################################
#  C U S T O M E R   M O D E L
######################################################################
class Customer(db.Model, PersistentBase):
    """ 
    Class that represents a Customer
    
    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """

    ##################################################
    # Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64)) # Username
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    phone_number = db.Column(db.String(32), nullable=True)  # phone # is optional
    account_status = db.Column(db.String(64)) #create a column for customer status
    addresses = db.relationship('Address', backref='customer', lazy=True)

    ##################################################
    # INSTANCE METHODS
    ##################################################
    def __repr__(self):
        return "<Customer %r id=[%s]>" % (self.name, self.id)

    def serialize(self) -> dict:
        """ Serializes a Customer into a dictionary """
        customer = {
            "id": self.id,
            "name": self.name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "account_status": self.account_status,
            "addresses": []
        }
        for address in self.addresses:
            customer['addresses'].append(address.serialize())
        return customer

    def deserialize(self, data: dict):
        """ 
        Deserializes a Customer from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.first_name = data["first_name"]
            self.last_name = data["last_name"]
            self.email = data["email"]
            self.phone_number = data.get("phone_number")
            self.account_status = data["account_status"]
            # handle inner list of addresses
            address_list = data.get("addresses")
            for json_address in address_list:
                address = Address()
                address.deserialize(json_address)
                self.addresses.append(address)
        except KeyError as error:
            raise DataValidationError(
                "Invalid Customer: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Customer body of request contained bad or no data"
            )
        return self
    
    @classmethod
    @retry(
        HTTPError, 
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )
    def find_by_name(cls, name: str) -> list:
        """ Returns all Customers with the given last name

        :param name: the user name of the Customers you want to match
        :type name: str

        :return: a collection of Customers with that last name
        :rtype: list

        """
        logger.info("Processing last name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    @retry(
        HTTPError, 
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )
    def find_by_first_name(cls, first_name: str) -> list:
        """ Returns all Customers with the given first name

        :param first_name: the first name of the Customers you want to match
        :type first_name: str

        :return: a collection of Customers with that first name
        :rtype: list

        """
        logger.info("Processing first name query for %s ...", first_name)
        return cls.query.filter(cls.first_name == first_name)

    @classmethod
    @retry(
        HTTPError, 
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )
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
    @retry(
        HTTPError, 
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )
    def find_by_email(cls, email: str) -> list:
        """ Returns all Customers with the given email

        :param first_name: the first name of the Customers you want to match
        :type first_name: str

        :return: a collection of Customers with that first name
        :rtype: list
        """
        logger.info("Processing email query for %s ...", email)
        return cls.query.filter(cls.email == email)

    @classmethod
    @retry(
        HTTPError, 
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )
    def find_by_phone_number(cls, phone_number: str) -> list:
        """ Returns all Customers with the given phone_number

        :param phone_number: the number of the Customers you want to match
        :type phone_number: str

        :return: a collection of Customers with that phone_number
        :rtype: list
        """
        logger.info("Processing phone_number query for %s ...", phone_number)
        return cls.query.filter(cls.phone_number == phone_number)

    @classmethod
    @retry(
        HTTPError, 
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )
    def find_by_street(cls, street: str) -> list:
        """ Returns all Customers with the given addess
        """
        logger.info("Processing street address query for %s ...", street)
        q = cls.query.outerjoin(cls.addresses).filter(Address.street == street)
        return q.all()
    
    @classmethod
    @retry(
        HTTPError, 
        delay=RETRY_DELAY,
        backoff=RETRY_BACKOFF,
        tries=RETRY_COUNT,
        logger=logger,
    )
    def find_by_postalcode(cls, postalcode: str) -> list:
        """ Returns all customers with an address in the given zip code """
        logger.info("Processing postal code query for %s ...", postalcode)
        q = cls.query.outerjoin(cls.addresses).filter(Address.postalcode == postalcode)
        return q.all()
