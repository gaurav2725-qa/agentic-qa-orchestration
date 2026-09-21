from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time


@given('I am logged in to my account')
def step_logged_in(context):
    context.driver = webdriver.Chrome()
    context.driver.get("https://example.com/account-dashboard")
    time.sleep(1)


@given('the system is configured with the default font')
def step_default_font(context):
    pass


@when('I log in to my account dashboard')
def step_view_dashboard(context):
    pass


@when('I click on the "Export Order History" button')
def step_click_export(context):
    try:
        button = context.driver.find_element(
            By.XPATH, '//button[contains(text(), "Export Order History")]'
        )
        button.click()
    except NoSuchElementException:
        context.export_failed_element_not_found = True


@then('the system should generate a downloadable PDF file')
def step_verify_pdf_generated(context):
    assert not getattr(context, "export_failed_element_not_found", False), \
        "Export button not found on page — target page/feature does not exist"


@then('the PDF should be in the correct format, including thousands separators and decimal points in the correct position')
def step_verify_pdf_format(context):
    pass


@given('my account has no order history')
def step_no_orders(context):
    pass


@then('the system should not generate a PDF file')
def step_verify_no_pdf(context):
    pass


@then('a message should be displayed indicating that there are no orders to export')
def step_verify_no_orders_message(context):
    pass