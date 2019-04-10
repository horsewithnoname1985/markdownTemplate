*** Settings ***
Documentation   Check the generated template files have correct content
Suite Setup     application is started
Test Setup      new form is filled with valid data

#Resource        ${EXECDIR}/Resources/_Steps/STPS_TemplateContent.robot
#Resource        ${EXECDIR}/Resources/_Steps/STPS_Form.robot
Resource        ${EXECDIR}/Resources/_Units/form.robot
Resource        ${EXECDIR}/Resources/_Units/browser.robot
Resource        ${EXECDIR}/Resources/_Units/template_creation.robot
Resource        ${EXECDIR}/Resources/_SetupTeardown/STPTD_mdtemplate.robot

*** Test Cases ***
Script files refer to correct files
    [Tags]
    When the user form is submitted
    Then the resulting script files reference the correct template files

Markdown template has correct content
    When the user form is submitted
    Then the resulting markdown file contains the correct content
