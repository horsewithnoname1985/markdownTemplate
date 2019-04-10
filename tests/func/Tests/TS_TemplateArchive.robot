*** Settings ***
Documentation   Suite description

#Resource        ${EXECDIR}/Resources/_Steps/STPS_TemplateArchive.robot
#Resource        ${EXECDIR}/Resources/_Steps/STPS_Form.robot
Resource        ${EXECDIR}/Resources/_SetupTeardown/STPTD_mdtemplate.robot
Resource        ${EXECDIR}/Resources/_Units/form.robot
Resource        ${EXECDIR}/Resources/_Units/browser.robot
Resource        ${EXECDIR}/Resources/_Units/template_creation.robot

Suite Setup     application is started
Test Setup      new form is filled with valid data

#*** Test Cases ***
#Correct template files are downloaded
#    [Setup]     Start app and open url
#    [Teardown]  Close browser and app
#    Given the user form is displayed
#    And the Robot Framework style is selected
#    And the English language is selected
#    When the user form is submitted
#    Then the correct template files reside in the download archive

*** Test Cases ***
Archive contains correct predefined template files
    [Tags]    DEBUG
    Given the English language is selected
    And the RobotFramework style template is selected
    When the user form is submitted
    Then the selected files reside in the resulting archive

Archive file contains all required files
    [Tags]    nothing
    When the user form is submitted
    Then all template files reside in the resulting archive