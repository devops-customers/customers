# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for Customer Model

Test cases can be run with:
    nosetests
    coverage report -m

While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_models.py:TestCustomerModel

"""
from ctypes import addressof
import os
import logging
import unittest
from service.models import Customer, Address, DataValidationError, db
from service import app
from .factories import CustomerFactory, AddressFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  C U S T O M E R   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestCustomerModel(unittest.TestCase):
    """Test Cases for Customer Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Customer.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  H E L P E R   M E T H O D S
    ###################################################################### 

    def _create_customer(self, addresses=[]):
        """ Creates a Customer from a Factory """
        fake_customer = CustomerFactory()
        customer = Customer(
            name = fake_customer.name,
            first_name = fake_customer.first_name,
            last_name = fake_customer.last_name, 
            email = fake_customer.email,
            phone_number = fake_customer.phone_number,
            addresses = addresses
        )
        self.assertTrue(customer != None)
        self.assertEqual(customer.id, None)
        return customer 

    def _create_address(self):
        """ Creates fake address from factory """ 
        fake_address = AddressFactory()
        address = Address(
            name=fake_address.name,
            street=fake_address.street,
            city=fake_address.city,
            state=fake_address.state,
            postalcode=fake_address.postalcode
        )
        self.assertTrue(address != None)
        self.assertEqual(address.id, None)
        return address

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_customer(self):
        """ Create a Customer and assert that it exists """
        fake_customer = CustomerFactory()
        customer = Customer(
            name = fake_customer.name,
            first_name = fake_customer.first_name,
            last_name = fake_customer.last_name, 
            email = fake_customer.email,
            phone_number = fake_customer.phone_number
        )
        self.assertTrue(customer != None)
        self.assertEqual(customer.id, None)
        self.assertEqual(customer.name, fake_customer.name)
        self.assertEqual(customer.first_name, fake_customer.first_name)
        self.assertEqual(customer.last_name, fake_customer.last_name)
        self.assertEqual(customer.email, fake_customer.email)
        self.assertEqual(customer.phone_number, fake_customer.phone_number)

    def test_add_a_customer(self):
        """ Creates a customer and adds it to the database """
        customers = Customer.all()
        self.assertEqual(customers, [])
        customer = self._create_customer()
        customer.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(customer.id, 1)
        customers = Customer.all()
        self.assertEqual(len(customers),1)

    def test_read_customer(self):
        """ Read a customer """
        customer = self._create_customer()
        customer.create()

        # Read it back
        found_customer = Customer.find(customer.id)
        self.assertEqual(found_customer.id, customer.id)
        self.assertEqual(found_customer.name, customer.name)
        self.assertEqual(found_customer.first_name, customer.first_name)
        self.assertEqual(found_customer.last_name, customer.last_name)
        self.assertEqual(found_customer.email, customer.email)
        self.assertEqual(found_customer.phone_number, customer.phone_number)

    def test_update_customer(self):
        """ Update a customer """
        customer = self._create_customer()
        customer.create()
        # Assert that it was assigned an id and shows in the database
        self.assertEqual(customer.id, 1)

        # Fetch it back
        customer = Customer.find(customer.id)
        customer.email = "XXX@YYY.COM"
        customer.save()

        # Fetch it back again
        customer = Customer.find(customer.id)
        self.assertEqual(customer.email, "XXX@YYY.COM")

    def test_delete_a_customer(self):
        """ Delete a customer from the database """
        customers = Customer.all()
        self.assertEqual(customers, [])
        customer = self._create_customer()
        customer.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(customer.id, 1)
        customers = Customer.all()
        self.assertEqual(len(customers), 1)
        customer = customers[0]
        customer.delete()
        customers = Customer.all()
        self.assertEqual(len(customers), 0)

    def test_list_all_customers(self):
        """ List all Customers in the database """
        customers = Customer.all()
        self.assertEqual(customers, [])
        for _ in range(5):
            customer = self._create_customer()
            customer.create()
        # Assert that there are now 5 customers in the database
        customers = Customer.all()
        self.assertEqual(len(customers),5)

    def test_find_or_404(self):
        """ Find or throw 404 error """
        customer = self._create_customer()
        customer.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(customer.id, 1)

        # Fetch it back
        customer = Customer.find_or_404(customer.id)
        self.assertEqual(customer.id, 1)

    def test_find_by_name(self):
        """ Find by username """
        customer = self._create_customer()
        customer.create()

        # Fetch it back by name
        same_customer = Customer.find_by_name(customer.name)[0]
        self.assertEqual(same_customer.id, customer.id)
        self.assertEqual(same_customer.name, customer.name)

    def test_find_by_first_name(self):
        """ Find by first name """
        customer = self._create_customer()
        customer.create()

        # Fetch it back by name
        same_customer = Customer.find_by_first_name(customer.first_name)[0]
        self.assertEqual(same_customer.id, customer.id)
        self.assertEqual(same_customer.first_name, customer.first_name)

    def test_find_by_last_name(self):
        """ Find by last name """
        customer = self._create_customer()
        customer.create()

        # Fetch it back by name
        same_customer = Customer.find_by_last_name(customer.last_name)[0]
        self.assertEqual(same_customer.id, customer.id)
        self.assertEqual(same_customer.last_name, customer.last_name)

    def test_find_by_phone_number(self):
        """ Find by phone number """
        customer = self._create_customer()
        customer.create()

        # Fetch it back by name
        same_customer = Customer.find_by_phone_number(customer.phone_number)[0]
        self.assertEqual(same_customer.id, customer.id)
        self.assertEqual(same_customer.phone_number, customer.phone_number)

    def test_serialize_a_customer(self):
        """ Serialize a customer """
        address = self._create_address()
        customer = self._create_customer(addresses=[address])
        serial_customer = customer.serialize()
        self.assertEqual(serial_customer['id'], customer.id)
        self.assertEqual(serial_customer['name'], customer.name)
        self.assertEqual(serial_customer['first_name'], customer.first_name)
        self.assertEqual(serial_customer['last_name'], customer.last_name)
        self.assertEqual(serial_customer['email'], customer.email)
        self.assertEqual(serial_customer['phone_number'], customer.phone_number)
        self.assertEqual(len(serial_customer['addresses']), 1)
        addresses = serial_customer['addresses']
        self.assertEqual(addresses[0]['id'], address.id)
        self.assertEqual(addresses[0]['customer_id'], address.customer_id)
        self.assertEqual(addresses[0]['name'], address.name)
        self.assertEqual(addresses[0]['street'], address.street)
        self.assertEqual(addresses[0]['city'], address.city)
        self.assertEqual(addresses[0]['state'], address.state)
        self.assertEqual(addresses[0]['postalcode'], address.postalcode)

    def test_deserialize_a_customer(self):
        """ Deserialize a customer """ 
        address = self._create_address()
        customer = self._create_customer(addresses=[address])
        serial_customer = customer.serialize()
        new_customer = Customer()
        new_customer.deserialize(serial_customer)
        self.assertEqual(new_customer.id, customer.id)
        self.assertEqual(new_customer.first_name, customer.first_name)
        self.assertEqual(new_customer.last_name, customer.last_name)
        self.assertEqual(new_customer.email, customer.email)
        self.assertEqual(new_customer.phone_number, customer.phone_number)

    def test_deserialize_with_key_error(self):
        """ Deserialize a customer with a KeyError """
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, {})

    def test_deserialize_with_type_error(self):
        """ Deserialize a customer with a TypeError """
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, [])

    def test_deserialize_address_key_error(self):
        """ Deserialize an address with a KeyError """
        address = Address()
        self.assertRaises(DataValidationError, address.deserialize, {})

    def test_deserialize_address_type_error(self):
        """ Deserialize an address with a TypeError """
        address = Address()
        self.assertRaises(DataValidationError, address.deserialize, [])

    def test_add_customer_address(self):
        """ Create a customer with an address and add it to the database """
        customers = Customer.all()
        self.assertEqual(customers, [])
        customer = self._create_customer()
        address = self._create_address()
        customer.addresses.append(address)
        customer.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(customer.id, 1)
        customers = Customer.all()
        self.assertEqual(len(customers),1)

        new_customer = Customer.find(customer.id)
        self.assertEqual(new_customer.addresses[0].name, address.name)

        address2 = self._create_address()
        customer.addresses.append(address2)
        customer.update()

        new_customer = Customer.find(customer.id)
        self.assertEqual(len(customer.addresses), 2)
        self.assertEqual(new_customer.addresses[1].name, address2.name)

    def test_update_customer_address(self):
        """ Update a customer's address """
        customers = Customer.all()
        self.assertEqual(customers, [])

        address = self._create_address()
        customer = self._create_customer(addresses=[address])
        customer.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(customer.id, 1)
        customers = Customer.all()
        self.assertEqual(len(customers),1)

        # Fetch it back
        customer = Customer.find(customer.id)
        old_address = customer.addresses[0]
        self.assertEqual(old_address.city, address.city)

        old_address.city = "XX"
        customer.update()

        # Fetch it back again
        customer = Customer.find(customer.id)
        address = customer.addresses[0]
        self.assertEqual(address.city, "XX")

    def test_delete_customer_address(self):
        """ Delete a customer's address """
        customers = Customer.all()
        self.assertEqual(customers, [])

        address = self._create_address()
        customer = self._create_customer(addresses=[address])
        customer.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(customer.id, 1)
        customers = Customer.all()
        self.assertEqual(len(customers),1)

        # Fetch it back
        customer = Customer.find(customer.id)
        address = customer.addresses[0]
        address.delete()
        customer.update()

        # Fetch it back again
        customer = Customer.find(customer.id)
        self.assertEqual(len(customer.addresses),0)

    # Need a test of address __repr__ method
    # Need a test of address __str__ method
    # Need a test of address.serialize
    # Need a test of address.deserialize method

    # Need a test of customer.serialize
    # Need a test of customer.deserialize
    # Need a test of find_by_address

    # def test_find_by_address(self):
    #     """ Find by address """
    #     customer = self._create_customer()
    #     address = self._create_address()
    #     customer.addresses.append(address)
    #     customer.create()

    #     # Fetch it back by name
    #     same_customer = Customer.find_by_address(customer.addresses)[0]
    #     self.assertEqual(same_customer.id, customer.id)
    #     self.assertEqual(same_customer.addresses, customer.addresses)

    def test_find_by_street(self):
        """ Find by street address """
        customer = self._create_customer()
        address = self._create_address()
        customer.addresses.append(address)
        customer.create()

        same_customer = Customer.find_by_street(address.street)
        logging.debug(same_customer[0])
        self.assertEqual(same_customer[0], customer)
