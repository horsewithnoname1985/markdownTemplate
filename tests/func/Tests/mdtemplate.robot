*** Settings ***
Documentation       mdtemplate test suite
Library             SeleniumLibrary
Library             ../Libraries/app_runner.py

Metadata            Version     1.0
Metadata            Author      Arne Wohletz

*** Variables ***
${APP_URL}  empty


*** Test Cases ***
Browser displays form automatically
    [Tags]    app_launch
    Given the browser is closed
    When the application is launched
    And the application url is opened
    Then the user form is displayed

*** Keywords ***
the browser is closed
    close all browsers

the application is launched
    ${APP_URL}=  launch application

the application url is opened
    ${APP_URL}=  127.0.0.1:5000
    open browser  url=${APP_URL}  browser=firefox
#    go to  ${APP_URL}

the user form is displayed
    page should contain  Welcome to the markdown template creation!