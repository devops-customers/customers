Feature: The customers service back-end
    As a Customer Website
    I need a RESTful catalog service
    So that I can log all my customers

Background:
    Given the following customers
        | firstname   | lastname   | email_id         | address          | phone_number   | active   |
        | Jenna        | Yanish      | jy12@gmail.com   | 12th Street  | 100988814   | True     |
        | Nora       | BB   | nbb14@gmail.com   | 14th Street      | 999988814   | True     |
        | Winny       | Wu      | ww13@gmail.com   | 13th Street       | 222333444   | False    |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customers RESTful Service" in the title
    And I should not see "404 Not Found"