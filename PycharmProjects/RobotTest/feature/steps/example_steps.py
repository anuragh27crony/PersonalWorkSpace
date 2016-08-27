from behave import *

@given("Add 10 to data")
def step_add_data(context):
    pass

@when("Value of Data is 100")
def step_value_of_data(context):
    print("Inside when")

@then("Data should be equal to 110")
def step_data_should_be_equal(context):
    print("Inside the then")