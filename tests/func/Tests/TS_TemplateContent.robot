*** Settings ***
Documentation   Check the TemplateCreator functionality
Test Setup      Start app and open url
Test Teardown   Close browser and app

Resource        ${EXECDIR}/Resources/_Steps/STPS_TemplateFiles.robot
Resource        ${EXECDIR}/Resources/_Steps/STPS_Form.robot


*** Test Cases ***
Script files refer to correct files
    [Tags]
    Given the entire form is filled with data
    When the user form is submitted
    Then the resulting script files reference the correct template files

Markdown template has correct content
    Given all form data is entered
    When the user form is submitted
    Then the resulting markdown file contains the correct content
