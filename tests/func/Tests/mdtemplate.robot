*** Settings ***
Documentation    mdtemplate test suite
Library         SeleniumLibrary

*** Test Cases ***
Browser displays form automatically
    [Tags]    DEBUG
    Given the browser is closed
    When the application is launched
    And the application url is opened
    Then the user form is displayed

*** Keywords ***
the browser is closed
    Setup system under test

the application is launched

the browser is launched
    Se
the user form is displayed