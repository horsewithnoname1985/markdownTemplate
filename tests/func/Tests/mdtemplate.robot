*** Settings ***
Documentation       mdtemplate test suite
Resource            ../Resources/_Steps/STPS_mdtemplate.robot
Resource            ../Resources/_SetupTeardown/STPTD_mdtemplate.robot

Metadata            Version     1.0
Metadata            Author      Arne Wohletz

*** Variables ***
${APP_URL}  empty


*** Test Cases ***
Application is launched successfully
    [Tags]      app_launch
    [Teardown]  Close browser and app
    Given the browser is closed
    When the application is launched
    And the application url is opened
    Then the user form is displayed

All required fields must contain data to create download archive
    [Tags]      restriction
    [Setup]     Start app and open url
    [Teardown]  Close browser and app
    Given the user form is displayed
    When the create download button is clicked
    Then the download file is not created

#Download file is created when all fields contain data
#    [Tags]    restriction
#    [Setup]   Start app and open url
#    Given the user form is displayed
#    When all fields receive proper data
#    And the create download button is clicked
#    Then the download file is created
#    And the download file is offered for download
