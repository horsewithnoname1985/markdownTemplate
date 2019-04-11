*** Settings ***
Documentation   mdtemplate test suite
Resource        ${EXECDIR}/Resources/_SetupTeardown/STPTD_mdtemplate.robot
Resource        ${EXECDIR}/Resources/_Units/form.robot
Resource        ${EXECDIR}/Resources/_Units/browser.robot
Resource        ${EXECDIR}/Resources/_Units/template_creation.robot

Metadata            Version     1.0
Metadata            Author      Arne Wohletz

*** Variables ***
#${APP_URL}      empty

*** Test Cases ***
All required fields must contain data to create download archive
    [Tags]      restriction
    [Setup]     Start app and open url
    [Teardown]  Close browser and app
    Given the user form is displayed
    When the user form is submitted
    Then a warning message about missing user data is displayed
    And the download archive is not created

Download file is created when all fields contain data
    [Tags]      restriction  draft
    [Setup]     Start app and open url
    [Teardown]  Close browser and app
    Given the user form is displayed
    When the entire form is filled with valid data
    And the user form is submitted
    Then the archive file is offered for download

Download file is not created when required data is missing
    [Tags]      none
    [Setup]     Start app and open url
    [Teardown]  Close browser and app
    Given the user form is displayed
    When the entire form except the title is filled with valid data
    And the user form is submitted
    Then the archive file is not created
