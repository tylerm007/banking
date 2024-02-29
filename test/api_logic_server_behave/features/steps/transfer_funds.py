# this is the api_test.py
from behave import *
import requests, pdb
import json
from dotmap import DotMap
from test_utils import login
from sqlalchemy import insert


host = "localhost"
port = "5656"


"""
  Scenario: Transfer From Savings to Checking
    Given Transfer Transaction
      When Transfer submitted
      Then Rules Fire and Transaction Success    
"""

@given('Transfer Transaction')
def step_impl(context):
	assert True

@when('Transfer submitted')
def step_impl(context):
	#context.response_text = getAPI('Customer')
    scenario_name = 'Transfer From Savings to Checking'
    transfer_uri = f'http://localhost:5656/api/TransferFunds/transfer'
    transfer_args = {
        "meta": {
            "method": "Transfer",
            "args": {
                "FromAcctId": 7,
                "ToAcctId": 6,
                "Amount": 10
            }
        }
    }
    print(f'\n\n\n{scenario_name} - verify transfer...\n',scenario_name)
    r = requests.post(url=transfer_uri, json=transfer_args, headers=login())
    context.response_text = r.text
@then('Then Rules Fire and Transaction Success')
def step_impl(context):
    print(context.response_text)
    assert context.response_text.startswith("Transfer Completed amount")