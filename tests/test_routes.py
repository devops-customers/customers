"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from service import status  # HTTP Status Codes
from service.models import db
from service.routes import app, init_db

import os
import logging
import unittest

# from unittest.mock import MagicMock, patch
from urllib.parse import quote_plus
from service import app, status
from service.models import db, init_db
from .factories import CustomerFactory

# Disable all but critical errors during normal test run
# uncomment for debugging failing tests
logging.disable(logging.CRITICAL)

# DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/customers"
CONTENT_TYPE_JSON = "application/json"

######################################################################
#  T E S T   C A S E S
######################################################################


class TestYourResourceServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        pass

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        self.app = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        pass

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ Test index call """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # Test create customer account
    def test_create_a_customer(self):
        """Create a new Customer Account"""
        customer = CustomerFactory()
        logging.debug(customer)
        resp = self.app.post(
            BASE_URL, json=customer.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_customer = resp.get_json()
        self.assertEqual(
            new_customer["first_name"], customer.first_name,
            "First name does not match"
        )
        self.assertEqual(
            new_customer["last_name"], customer.last_name, "Last name does not match"
        )
        self.assertEqual(
            new_customer["email"], customer.email, "Email does not match"
        )
        self.assertEqual(
            new_customer["phone_number"], customer.phone_number, "Phone number does not match"
        )

        # Check that the location header was correct
        resp = self.app.get(location, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_customer = resp.get_json()
        self.assertEqual(
            new_customer["first_name"], customer.first_name,
            "First name does not match"
        )
        self.assertEqual(
            new_customer["last_name"], customer.last_name, "Last name does not match"
        )
        self.assertEqual(
            new_customer["email"], customer.email, "Email does not match"
        )
        self.assertEqual(
            new_customer["phone_number"], customer.phone_number, "Phone number does not match"
        )

    # Test create customer account with missing data
    def test_create_a_customer_no_data(self):
        """Create a Customer with missing data"""
        resp = self.app.post(BASE_URL, json={}, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

  # Test update the customer
    def test_update_customer(self):
        """Update an existing customer"""
        # create a customer to update
        test_customer = CustomerFactory()
        resp = self.app.post(
            BASE_URL, json=test_customer.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the customer
        new_customer = resp.get_json()
        logging.debug(new_customer)
        new_customer["category"] = "unknown"
        resp = self.app.put(
            "/customer/{}".format(new_customer["id"]),
            json=new_customer,
            content_type=CONTENT_TYPE_JSON,
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_customer = resp.get_json()
        self.assertEqual(updated_customer["category"], "unknown")

    def test_get_customer(self):
        """Get a single customer"""
        # get the id of a customer
        test_customer = self._create_customers(1)[0]
        resp = self.app.get(
            "/customers/{}".format(test_customer.id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], test_customer.name)

    def test_get_customer_not_found(self):
        """Get a customer thats not found"""
        resp = self.app.get("/customers/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
