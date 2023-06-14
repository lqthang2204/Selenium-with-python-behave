@test
Feature: navigate URL
  Scenario: test login page
    Given I navigate to "https://demo.openmrs.org/openmrs/login.htm"
    And I change the page spec to LoginPage
    And I wait for element user-field to be DISPLAYED
    And I wait for element pass-field to be DISPLAYED
    And I type "Admin" into element user-field
    And I type "Admin123" into element pass-field
    And I perform login-page action
    And I change the page spec to IndexPage
    And I wait for element welcome-user to be DISPLAYED
    And I wait for element log-out to be DISPLAYED
#    And I type "Admidsdsdsn" into element user-field
#    And I type "Admin12dsdsds3" into element pass-field
#    And I click element location-option-inpatient
#    And I wait for element login-button to be ENABLED
#    And I click element login-button
#    And I wait for element error-message to be DISPLAYED
#    And I verify the text for element error-message is "Invalid username/password. Please try again."
#    And I verify the text for element error-message is "Usuario/contraseña inválida. Por favor inténtelo nuevamente."
#    And I navigate to refresh-page
#    And I type "Admin" into element user-field
#    And I type "Admin123" into element pass-field
#    And I save text for element location-option-inpatient with key "location"
#    And I click element location-option-inpatient
#    And I click element login-button