*** Settings ***
Documentation       Keywords concerning the user form interactions
Library             SeleniumLibrary


*** Keywords ***
the create download button is clicked
    click button    ${XPATH_CREATE_TEMPLATE_BUTTON}

the download file is not created
    alert should be present    Please fill out all mandatory fields

all fields receive proper data
