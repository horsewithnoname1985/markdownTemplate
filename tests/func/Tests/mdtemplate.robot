*** Settings ***
Documentation       mdtemplate test suite
Library             SeleniumLibrary
Library             ../Libraries/app_runner.py

Metadata            Version     1.0
Metadata            Author      Arne Wohletz

*** Test Cases ***
Browser displays form automatically
    [Tags]    DEBUG
    Given the browser is closed
    When the application is launched
    And the application url is opened
    Then the user form is displayed

*** Keywords ***
the browser is closed
    close all browsers

the application is launched
    ${app_url} =  launch application

the application url is opened
    go to user form  ${app_url}

the user form is displayed
    page should contain  Welcome to the markdown template creation!