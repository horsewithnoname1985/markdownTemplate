*** Settings ***
Resource        ${EXECDIR}/Resources/_Units/application.robot
Resource        ${EXECDIR}/Resources/_Units/browser.robot
Resource        ${EXECDIR}/Resources/_Units/form.robot

Suite Setup     application is started
Test Setup      new form is filled with valid data

*** Keywords ***
the ${language} language is selected

the ${style} style template is selected



*** Test Cases ***
Archive contains correct predefined template files
    [Tags]    DEBUG
    Given all form data is entered
    And the English language is selected
    And the RobotFramework style template is selected
    When the user form is submitted
    Then the correct files reside in the resulting archive

Archive file contains all required files
    [Tags]    nothing
    Given all form data is entered
    When the user form is submitted
    Then all required files reside in the resulting archive