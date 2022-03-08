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