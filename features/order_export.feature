Feature: Export Order History as PDF

  As a registered customer, I want to be able to export my
  complete order history as a downloadable PDF, so I can
  easily review and utilize the information.

  Scenario: Export Order History as PDF with Complete Information
    Given the system is configured with the default font
    Given I am logged in to my account
    When I log in to my account dashboard
    And I click on the "Export Order History" button
    Then the system should generate a downloadable PDF file
    And the PDF should be in the correct format, including thousands separators and decimal points in the correct position

  Scenario: Edge: Empty Order History
    Given my account has no order history
    Given I am logged in to my account
    When I log in to my account dashboard
    And I click on the "Export Order History" button
    Then the system should not generate a PDF file
    And a message should be displayed indicating that there are no orders to export