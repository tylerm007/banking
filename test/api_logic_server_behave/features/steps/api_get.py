# this is the api_test.py
from behave import *
import requests, pdb
import json
from dotmap import DotMap
from test_utils import login

host = "localhost"
port = "5656"

def getAPI(table_name:str):
	get_uri = f'http://{host}:{port}/api/{table_name}?'\
	"page%5Boffset%5D=0&page%5Blimit%5D=1"
	r = requests.get(url=get_uri, headers= login())
	result_data = json.loads(r.text)
	if r.status_code == 500:
		raise requests.exceptions.HTTPError(f"API Exception on {get_uri}")
	return DotMap(result_data)

def patchAPI(table_name:str, payload:dict, key:any):
	get_uri = f'http://{host}:{port}/api/{table_name}/{key}'
	r = requests.patch(url=get_uri, json=payload, headers= login())
	return json.loads(r.text)


@given('GET Customer endpoint')
def step_impl(context):
	assert True

@when('GET Customer API')
def step_impl(context):
	context.response_text = getAPI('Customer')

@then('Customer retrieved')
def step_impl(context):
	response_text = context.response_text
	assert len(response_text.data) > 0

@given('GET Branch endpoint')
def step_impl(context):
	assert True

@when('GET Branch API')
def step_impl(context):
	context.response_text = getAPI('Branch')

@then('Branch retrieved')
def step_impl(context):
	response_text = context.response_text
	assert len(response_text.data) > 0

@given('GET AccountType endpoint')
def step_impl(context):
	assert True

@when('GET AccountType API')
def step_impl(context):
	context.response_text = getAPI('AccountType')

@then('AccountType retrieved')
def step_impl(context):
	response_text = context.response_text
	assert len(response_text.data) > 0

@given('GET Account endpoint')
def step_impl(context):
	assert True

@when('GET Account API')
def step_impl(context):
	context.response_text = getAPI('Account')

@then('Account retrieved')
def step_impl(context):
	response_text = context.response_text
	assert len(response_text.data) > 0

@given('GET Transfer endpoint')
def step_impl(context):
	assert True

@when('GET Transfer API')
def step_impl(context):
	context.response_text = getAPI('Transfer')

@then('Transfer retrieved')
def step_impl(context):
	response_text = context.response_text
	assert len(response_text.data) > 0

@given('GET Employee endpoint')
def step_impl(context):
	assert True

@when('GET Employee API')
def step_impl(context):
	context.response_text = getAPI('Employee')

@then('Employee retrieved')
def step_impl(context):
	response_text = context.response_text
	assert len(response_text.data) > 0

@given('GET Transaction endpoint')
def step_impl(context):
	assert True

@when('GET Transaction API')
def step_impl(context):
	context.response_text = getAPI('Transaction')

@then('Transaction retrieved')
def step_impl(context):
	response_text = context.response_text
	assert len(response_text.data) > 0
