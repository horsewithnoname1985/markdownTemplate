*** Settings ***
Documentation   Setup and teardown keywords for mdtemplate
Resource        ${EXECDIR}/Resources/_LibraryAdapters/SeleniumLibraryAdapter.robot
Resource        ${EXECDIR}/Resources/_LibraryAdapters/ApplicationLibraryAdapter.robot
Resource        ${EXECDIR}/Resources/_LibraryAdapters/FormLibraryAdapter.robot
#Resource        ${EXECDIR}/Resources/

*** Variables ***
${XPATH_CREATE_TEMPLATE_BUTTON}    xpath://html/body/div[1]/form/input


*** Keywords ***
application is started
    ${APP_URL}=    launch application
    set test variable    ${APP_URL}

start app and open url
    close browser
    application is started
#    ${APP_URL}=    launch application
#    set test variable    ${APP_URL}
    open browser         ${APP_URL}

close browser and app
    shutdown application
    close browser

new form is filled with valid data
    open browser         ${APP_URL}
    fill out form using proper data
