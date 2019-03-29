*** Settings ***
Documentation   Setup and teardown keywords for mdtemplate
#Resource        ${EXECDIR}/func/Resources/_Steps/STPS_application.robot
Resource        ${EXECDIR}/func/Resources/_Units/browser.robot
Resource        ${EXECDIR}/func/Resources/_Units/application.robot
#Library         ${EXECDIR}/func/Libraries/app_runner.py
#Library         SeleniumLibrary
Resource        ${EXECDIR}/func/Resources/_LibraryAdapters/SeleniumLibraryAdapter.robot
#Resource        ${EXECDIR}/func/Resources/_LibraryAdapters/ApplicationLibraryAdapter.robot

*** Variables ***
${XPATH_CREATE_TEMPLATE_BUTTON}    xpath://html/body/div[1]/form/input


*** Keywords ***
Start app and open url
    the browser is closed
    ${APP_URL}=    the application is launched
    the application url is opened    ${APP_URL}

Close browser and app
    shutdown application
    close browser
