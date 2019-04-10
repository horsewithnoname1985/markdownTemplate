*** Settings ***
Documentation   user form steps

Resource        ${EXECDIR}/Resources/_Units/form.robot

*** Keywords ***
the user form is displayed
    browser displays form page
