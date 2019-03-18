*** Settings ***
Documentation   Suite description
Resource        ${EXECDIR}/func/Resources/_Steps/STPS_application.robot
Library         ${EXECDIR}/func/Libraries/app_runner.py
Library         SeleniumLibrary


*** Variables ***
${XPATH_CREATE_TEMPLATE_BUTTON}    xpath://html/body/div[1]/form/input


*** Keywords ***
Start app and open url
    the browser is closed
    the application is launched
    the application url is opened

Close browser and app
    shutdown application
    close browser
