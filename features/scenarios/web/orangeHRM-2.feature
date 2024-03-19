@regression @web
Feature: orange HRM 2 web

#  @Windows10_Chrome_76.0
#  @Windows10_Firefox_68.0
  Scenario: negative to url2
    Given I navigate to url GOOGLE
    And I change the page spec to pageGoogle
    And I wait for element search-field to be DISPLAYED
    And I click element search-field
    And I type "lqthang" into element search-field
    And I navigate to url TECHPANDA
    And I change the page spec to HomePage
    And I wait for element mobile-button to be DISPLAYED
    And I wait for element mobile-button to be ENABLED
    And I wait for element mobile-button to be EXISTED
    And I click element mobile-button
    And I type "test" into element search-input

#  Scenario: This will not be included
#    Given I navigate to url have index 1
#    And I change the page spec to LoginPage
#    And I wait for element user-field to be DISPLAYED
#    And I wait for element pass-field to be DISPLAYED
#    And I type "Admin" into element user-field

  @test2
  Scenario: test login page2
    Given I navigate to url OPEN_MRS
    And I change the page spec to LoginPage
    And I wait for element user-field to be DISPLAYED
    And I wait for element pass-field to be DISPLAYED
    And I type "Admin" into element user-field
    And I type "Admin123" into element pass-field
    And I perform login-page action
    And I change the page spec to IndexPage
#    And I wait for element welcome-user to be DISPLAYED
#    And I wait for element log-out to be DISPLAYED

#  Scenario: This is commented script
#    Given I navigate to url have index 1
#    And I change the page spec to LoginPage
#    And I wait for element user-field to be DISPLAYED
#    And I wait for element pass-field to be DISPLAYED
#    And I type "Admin" into element user-field

  @norun
  Scenario: This should not be included
    Given I navigate to url OPEN_MRS
    And I change the page spec to LoginPage
    And I wait for element user-field to be DISPLAYED
    And I wait for element pass-field to be DISPLAYED
    And I type "Admin" into element user-field

      @keyboard-1
  Scenario: execute keyboard with element
    Given I navigate to url OPEN_MRS
    And I change the page spec to LoginPage
    And I wait for element user-field to be DISPLAYED
    And I wait for element pass-field to be DISPLAYED
    And I type "Admin" into element user-field
    And I click keyboard NUMPAD1 button on element user-field
        And I wait 50 seconds

      @keyboard-2
  Scenario: execute keyboard without element
    Given I navigate to url OPEN_MRS
    And I change the page spec to LoginPage
    And I wait for element user-field to be DISPLAYED
    And I wait for element pass-field to be DISPLAYED
    And I type "Admin" into element user-field
    And I execute KEY_DOWN with keyboard CONTROL+a
    And I execute KEY_DOWN with keyboard CONTROL+c
    And I click element pass-field
    And I execute KEY_DOWN with keyboard CONTROL+v
    And I wait 50 seconds