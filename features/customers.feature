Feature: The customers service back-end
    As a Customer Website
    I need a RESTful catalog service
    So that I can log all my customers

Background:
    Given the following customers
        | firstname   | lastname   | email         |    account_status      | phone_number   |
        | Jenna        | Yanish      | jy12@gmail.com   | active  | 1009888141   |
        | Nora       | BB   | nbb14@gmail.com   |    active  | 9999888141   | 
        | Winny       | Wu      | ww13@gmail.com   |   active   | 2223331444   |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customers RESTful Service" in the title
    And I should not see "404 Not Found"