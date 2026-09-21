Feature: Secure Login with Error Handling and Session Management

  Scenario: Successful Login with Valid Credentials
    Given user "tomsmith" logged in with password "SuperSecretPassword!"
    When login button is clicked
    Then redirect to secure area and success message is displayed

  Scenario: Zero Length Username with Error Message
    Given username as empty string
    When login button is clicked
    Then error message is displayed indicating invalid username

  Scenario: Maximum Password Length with Error Message
    Given password length exceeds maximum allowed limit
    When login button is clicked
    Then error message is displayed indicating password length is too high

  Scenario: Empty Password Field with Error Message
    Given password field left empty or contains only whitespace
    When login button is clicked
    Then error message is displayed indicating required password

  Scenario: No Session Available Redirects to Login Page
    Given a user is not logged in
    When the user tries to access the secure area directly
    Then the user is redirected to the login page