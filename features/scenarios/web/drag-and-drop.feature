@web @regression @drag-drop
Feature: test feature drag and drop

  @drag-drop-1
  Scenario: test drag and drop 1
    Given I navigate to url GURU99
    And I change the page spec to demoguru99
    And I wait for element bank_label to be DISPLAYED
    And I wait for element debit_side to be DISPLAYED
#    And I hover-over element bank_label
    And I drag and drop element bank_label to element debit_side
    And I wait 5 seconds

#  @drag-drop-2
#  Scenario: test drag and drop 2
#    Given I navigate to url GLOBAL_SQA
#    And I change the page spec to drag_global
#    And I wait for element image with text "High Tatras" to be DISPLAYED
#    And I wait for element debit_side to be DISPLAYED
#    And I hover-over element bank_label
#    And I drag and drop element bank_label to element debit_side
#    And I wait 5 seconds

    @scroll-to-element-1
  Scenario: test scroll to element
    Given I navigate to url INDEX_GURU
    And I change the page spec to index_guru
    And I verify that following elements with below attributes
      | Field                  | Value  | Status    | Helpers |
      | header-python-tutorial | Python | DISPLAYED |         |
      And I wait 10 seconds

   @scroll-to-element-2
  Scenario: test scroll to element 2
    Given I navigate to url INDEX_GURU
    And I change the page spec to index_guru
    And I scroll by java-script to element header-python-tutorial
     And I wait 10 seconds
     And I scroll to element python-tutorial with text "Execute Python"
     And I wait 10 seconds
     And I scroll to element header-python-tutorial
     And I wait 10 seconds


      @right-and-double-click
  Scenario: action right and double cliclk
   Given I navigate to url GURU99-DOUBLE
    And I change the page spec to double-example
    And I wait for element double-button to be ENABLED
    And I double-click element double-button
    And I wait 2 seconds
    And I accept for popup
     And I double-click element double-button
    And I wait 2 seconds
    And I dismiss for popup
    And I right-click element right-button
    And I wait for element edit-button to be DISPLAYED





