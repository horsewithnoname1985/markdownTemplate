*** Settings ***
Documentation   Suite description

Resource        ${EXECDIR}/Resources/_Steps/STPS_Archive.robot
Resource        ${EXECDIR}/Resources/_Steps/STPS_Form.robot
Resource        ${EXECDIR}/Resources/_SetupTeardown/STPTD_mdtemplate.robot

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