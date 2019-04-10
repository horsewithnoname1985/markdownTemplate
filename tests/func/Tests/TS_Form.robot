*** Settings ***
Documentation       mdtemplate test suite
Resource            ${EXECDIR}/Resources/_SetupTeardown/STPTD_mdtemplate.robot
Resource            ${EXECDIR}/Resources/_Steps/STPS_mdtemplate.robot

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
    Then the download archive is not created

Download file is created when all fields contain data
    [Tags]      restriction   draft
    [Setup]     Start app and open url
    [Teardown]  Close browser and app
    Given the user form is displayed
    When all form fields are filled out
    And the user form is submitted
    Then the archive file is offered for download

Download file is not created when required data is missing
    [Tags]      none
    [Setup]     Start app and open url
    [Teardown]  Close browser and app
    Given the user form is displayed
    When all form fields except author are filled out
    And the user form is submitted
    Then the archive file is not created

Correct template files are downloaded
    [Setup]     Start app and open url
    [Teardown]  Close browser and app
    Given the user form is displayed
    And the Robot Framework style is selected
    And the English language is selected
    When the user form is submitted
    Then the correct template files reside in the download archive