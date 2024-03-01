# this is the api_test.py
from behave import *
import requests, pdb
import json
from dotmap import DotMap
from test_utils import login, prt
from sqlalchemy import insert


host = "localhost"
port = "5656"
scenario_name = 'Transfer From Savings to Checking'

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
    """
        Account.BALANCE is sum(Transaction.TotalAmount)
        Transaction.TotalAmount is Deposit less Withdrawal
        Transfer.FromAccountID Withdrawal Amount into Transaction
        Transfer.ToAccountID Deposit Amount into Transaction

    """
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

    r = requests.post(url=transfer_uri, json=transfer_args, headers=login())
    context.response_text = r.text
    context.status_code = r.status_code
@then('Rules Fire and Transaction Success')
def step_impl(context):
    print(context.response_text)
    print(context.status_code)
    prt(f'\n\n\n{scenario_name} - verify transfer...\n',scenario_name)
    assert context.status_code == 200
    #context.response_text["meta"]["result"][0].startswith("Transfer Completed amount")