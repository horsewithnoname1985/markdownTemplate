*** Settings ***
Documentation   Suite description

Resource        ${EXECDIR}/Resources/_SetupTeardown/STPTD_mdtemplate.robot
Resource    ${EXECDIR}/Resources/_Units/application.robot
Resource    ${EXECDIR}/Resources/_Units/browser.robot

*** Test Cases ***
Application is launched successfully
    [Tags]      app_launch
    [Teardown]  Close browser and app
    When the application is launched
    And the application url is opened
    Then the user form is displayed
