Feature: The customers service back-end
    As a Customer Website
    I need a RESTful catalog service
    So that I can log all my customers

Background:
    Given the following customers
    | name       | first_name  | last_name   | email           | phone_number    | account_status   |  addresses  |
    | annie123   | Annie       | Banana      | 123@gmail.com   | 6513466036      | True             |             |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customer RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Customer
    When I visit the "Home Page"
    And I set the "name" to "AnnieBanana"
    And I set the "first name" to "Annie"
    And I set the "last name" to "Banana"
    And I set the "email" to "123@gmail.com"
    And I set the "phone number" to "6513466036"
    And I set the "account status" to "active"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "id" field
    And I press the "Clear" button
    Then the "id" field should be empty
    And the "first name" field should be empty
    And the "last name" field should be empty
    And the "email" field should be empty
    And the "phone number" field should be empty
    And the "account status" field should be empty
    When I paste the "id" field
    And I press the "Retrieve" button
    Then I should see "AnnieBanana" in the "name" field
    Then I should see "Annie" in the "first name" field
    Then I should see "Banana" in the "last name" field
    Then I should see "123@gmail.com" in the "email" field
    Then I should see "6513466036" in the "phone number" field
    Then I should see "active" in the "account status" field

Scenario: Update Customer
    When I visit the "Home Page"
    And I set the "first_name" to "Annie"
    And I press the "search" button
    Then I should see "Annie" in the "first_name" field
    And I should see "Banana" in the "last_name" field
    And I should see "123@gmail.com" in the "email" field
    And I should see "6513466036" in the "phone_number" field
    Then I should see "active" in the "account_status" field
    When I change "phone_number" to "6513460000"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "id" field
    And I press the "Clear" button
    And I paste the "id" field
    And I press the "Retrieve" button
    Then I should see "6513460000" in the "phone_number" field
    When I press the "Clear" button
    And I set the "first_name" to "Annie"
    And I press the "Search" button
    Then I should see "6513460000" in the "phone_number" field
    And I should not see "6513466036" in the results