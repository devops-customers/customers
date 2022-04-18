import os
import json
import requests
from behave import given, when, then
from compare import expect

@given('the following customers')
def step_impl(context):
    """ Delete all Customers and load new ones """
    headers = {'Content-Type': 'application/json'}
    # list all of the customers and delete them one by one
    context.resp = requests.get(context.base_url + '/customers', headers=headers)
    expect(context.resp.status_code).to_equal(200)
    for customer in context.resp.json():
        context.resp = requests.delete(context.base_url + '/customers/' + str(customer["id"]), headers=headers)
        expect(context.resp.status_code).to_equal(204)
    
    # load the database with new customers
    create_url = context.base_url + '/customers'
    for row in context.table:
        data = {
           # "customer_id": row["customer_id"],
            "first_name": row['firstname'],
            "last_name": row['lastname'],
            "email": row['email'],
            "phone_number": row['phone_number'],
            "account_status": row['account_status'],
            }
        payload = json.dumps(data)
        context.resp = requests.post(create_url, data=payload, headers=headers)
        expect(context.resp.status_code).to_equal(201)