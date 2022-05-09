Feature: The addresses service back-end
    As a Customer Address Website
    I need a RESTful catalog service
    So that I can log all of my customer addresses

Background:
    Given the following customers
    | name       | first_name  | last_name   | email           | phone_number    | account_status   |  addresses  |
    | annie123   | Annie       | Banana      | 123@gmail.com   | 6513466036      | active           |             | 
    | roger123   | Roger       | Date        | 456@gmail.com   | 6561234567      | active           |             |
    | maya123    | Maya        | Orange      | 123@gmail.com   | 6562345678      | active           |             |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customer RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Address page is running
    When I visit the "Address Page"
    Then I should see "Customer Address RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create an Address for a Customer
    When I visit the "Home Page"
    And I set the "First Name" to "Annie"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "id" field
    And I visit the "Address Page"
    And I paste the "Address Customer Id" field
    And I set the "Address Name" to "Home"
    And I set the "Address Street" to "123 Fourth Street"
    And I set the "Address City" to "New York"
    And I select "New York" in the "Address State" dropdown
    And I set the "Address Postalcode" to "10001"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Address Customer id" field
    And I press the "Clear" button
    And I paste the "Address Customer id" field
    And I press the "List" button
    Then I should see the message "Success"
    And I should see "Home" in the "Address Name" field
    And I should see "123 Fourth Street" in the "Address Street" field
    And I should see "New York" in the "Address City" field

Scenario: Read/List a Customer Address
    When I visit the "Home Page"
    And I set the "First Name" to "Annie"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "id" field
    And I visit the "Address Page"
    And I paste the "Address Customer Id" field
    And I set the "Address Name" to "Home"
    And I set the "Address Street" to "123 Fourth Street"
    And I set the "Address City" to "New York"
    And I select "New York" in the "Address State" dropdown
    And I set the "Address Postalcode" to "10001"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Address Customer id" field
    And I press the "Clear" button
    And I paste the "Address Customer id" field
    And I set the "Address Name" to "Work"
    And I set the "Address Street" to "456 Seventh Ave."
    And I set the "Address City" to "New York"
    And I select "New York" in the "Address State" dropdown
    And I set the "Address Postalcode" to "10004"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Address Customer id" field
    And I press the "Clear" button
    And I paste the "Address Customer id" field
    And I press the "List" button
    Then I should see the message "Success"
    And I should see "Home" in the results
    And I should see "Work" in the results
    And I should not see "Vacation" in the results

Scenario: Update a Customer Address
    When I visit the "Home Page"
    And I set the "First Name" to "Annie"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "id" field
    And I visit the "Address Page"
    And I paste the "Address Customer Id" field
    And I set the "Address Name" to "Home"
    And I set the "Address Street" to "123 Fourth Street"
    And I set the "Address City" to "New York"
    And I select "New York" in the "Address State" dropdown
    And I set the "Address Postalcode" to "10001"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Address Customer id" field
    And I press the "Clear" button
    And I paste the "Address Customer id" field
    And I press the "List" button
    Then I should see the message "Success"
    And I should see "Home" in the "Address Name" field
    And I should see "123 Fourth Street" in the "Address Street" field
    And I should see "New York" in the "Address City" field
    When I copy the "ID" field from the results
    And I paste the "Address id" field
    And I change "Address Name" to "Vacation"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Address Customer Id" field
    And I press the "Clear" button
    And I paste the "Address Customer Id" field
    And I press the "List" button
    Then I should see the message "Success"
    And I should see "Vacation" in the "Address Name" field

Scenario: Delete a Customer Address
    When I visit the "Home Page"
    And I set the "First Name" to "Annie"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "id" field
    And I visit the "Address Page"
    And I paste the "Address Customer Id" field
    And I set the "Address Name" to "Home"
    And I set the "Address Street" to "123 Fourth Street"
    And I set the "Address City" to "New York"
    And I select "New York" in the "Address State" dropdown
    And I set the "Address Postalcode" to "10001"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Address Customer id" field
    And I press the "Clear" button
    And I paste the "Address Customer id" field
    And I set the "Address Name" to "Work"
    And I set the "Address Street" to "456 Seventh Ave."
    And I set the "Address City" to "New York"
    And I select "New York" in the "Address State" dropdown
    And I set the "Address Postalcode" to "10004"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Address Customer id" field
    And I press the "Clear" button
    And I paste the "Address Customer id" field
    And I press the "List" button
    Then I should see the message "Success"
    When I press the "Clear" button
    And I copy the "ID" field from the results
    And I paste the "Address id" field
    And I copy the "Customer ID" field from the results
    And I paste the "Address Customer id" field
    And I press the "Delete" button
    Then I should see the message "Address has been Deleted!"
    When I copy the "Customer ID" field from the results
    And I press the "Clear" button
    And I paste the "Address Customer id" field
    And I press the "List" button
    Then I should see the message "Success"
    And I should not see "Home" in the results
    And I should see "Work" in the results