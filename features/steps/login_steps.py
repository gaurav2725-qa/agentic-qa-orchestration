from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By


@given('I open the login page')
def step_open_login_page(context):
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    context.driver = webdriver.Chrome(options=options)
    context.driver.get("https://the-internet.herokuapp.com/login")


@given('user "{user}" logged in with password "{password}"')
def step_login_with_credentials(context, user, password):
    context.driver.find_element(By.ID, "username").send_keys(user)
    context.driver.find_element(By.ID, "password").send_keys(password)
    context.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()


@when('login button is clicked')
def step_click_login_already_done(context):
    pass  # login already performed in the Given step above


@then('redirect to secure area and success message is displayed')
def step_verify_success(context):
    success_message = context.driver.find_element(By.CSS_SELECTOR, ".flash.success")
    assert success_message.is_displayed(), "Success message not displayed"
    assert "/secure" in context.driver.current_url, "Did not redirect to secure area"