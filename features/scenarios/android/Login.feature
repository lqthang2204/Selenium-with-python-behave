@test @mobile
Feature: login mobile

  Scenario: test login page2 mobile
    Given I navigate to url OPEN_MRS
    And I change the page spec to LoginPage
    And I wait for element user-field to be DISPLAYED
    And I wait for element pass-field to be DISPLAYED
    And I type "Admin" into element user-field
    And I type "Admin123" into element pass-field
    And I click element login-button

 @switch-Iframe-android
  Scenario: switch-Iframe
    Given I navigate to url GURU99-DOUBLE
    And I change the page spec to double-example
#   And I wait for element selenium-button to be ENABLED
    And I click element selenium-button
#    And I wait for element selenium-demo-page to be ENABLED
#   And I wait for element selenium-demo-page to be ENABLED
    And I click element selenium-demo-page
#    And I perform click-if-exist-button action
    And I wait for element banner-jmeter to be ENABLED
    And I scroll to element banner-jmeter
    And I click element banner-jmeter
    And I switch active tab with index 2
    And I switch active tab with title "Selenium Live Project: FREE Real Time Project for Practice"
    And I change the page spec to Selenium_Live_Project
    And I verify that following elements with below attributes
      | Field        | Value                                                      | Status    | Helpers |
      | title_header | Selenium Live Project: FREE Real Time Project for Practice | DISPLAYED |         |
    And I wait 5 seconds

   @scroll_element_android
  Scenario: Scroll element demo android
    Given I change the page spec to indexRN
    And I wait for element product-one to be ENABLED
    And I click element product-one
    And I verify that following elements with below attributes
      | Field              | Value                | Status    | Helpers |
      | name-product       | Sauce Lab Back Packs | DISPLAYED |         |
      | Add-to-card-button | Add to cart          | ENABLED   |         |
#     And I wait for element Back-button to be ENABLED
#    And I click element Back-button
     And I wait 5 seconds
    And I scroll down to element product-six
    And I click element product-six
#    And I click element Back-button
     And I wait 5 seconds
     And I scroll up to element product-two
    And I scroll up to element product-one
    And I click element product-one
#    And I click element product-six
#    //XCUIElementTypeStaticText[@name="Sauce Labs Backpack"]
#    And I click element selenium-button
#    And I click element selenium-demo-page