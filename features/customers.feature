Feature: The customers service back-end
    As a Customer Website
    I need a RESTful catalog service
    So that I can log all my customers

Background:
    Given the following customers
        | firstname   | lastname   | email         | phone_number   |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customer RESTful Service" in the title
    And I should not see "404 Not Found"