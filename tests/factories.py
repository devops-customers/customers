# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
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
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice
from service.models import Customer, Address

class CustomerFactory(factory.Factory):
    """ Creates fake customers """

    class Meta: 
        """ Maps factory to data model """
        model = Customer

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    phone_number = factory.Faker("phone_number")

class AddressFactory(factory.Factory):
    """ Creates fake addresses """

    class Meta:
        model = Address
    
    id = factory.Sequence(lambda n: n)
    customer_id = factory.RelatedFactory(
        CustomerFactory
    #    factory_related_name='customer'
    )
    name = FuzzyChoice(choices = ["Home", "Work", "Vacation", "Other"])
    street = factory.Faker("street_address")
    city = factory.Faker("city")
    state = factory.Faker("state_abbr")
    postalcode = factory.Faker("postcode")