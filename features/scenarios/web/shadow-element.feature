@parallel @web @shadow
Feature: test shadow elements

  @mc-chrome-shadow
  Scenario: test shadow feature function
    Given I navigate to url CHROME-SETTING
    And I change the page spec to settingpage
    And I click shadow element import borkmarks
    And I click shadow element import button
    And I wait 5 seconds
    And I click shadow element toogle button
    And I wait 5 seconds

    @mc-chrome-shadow
  Scenario: test shadow feature function
    Given I navigate to url CHROME-SETTING
    And I change the page spec to settingpage
    And I click shadow element search field
    And I type "Customize your Chrome profile" into shadow element import button
    And I wait 5 seconds
    And I click shadow element toogle button
    And I wait 5 seconds
#    And I wait for element mobile-button to be DISPLAYED
#    And I click element <product>
#    And I type "test " into element search-input
#    And I wait 2 seconds