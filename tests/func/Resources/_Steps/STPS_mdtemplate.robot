*** Settings ***
Resource    ${EXECDIR}/func/Resources/_Units/application.robot
Resource    ${EXECDIR}/func/Resources/_Units/browser.robot
Resource    ${EXECDIR}/func/Resources/_Units/form.robot

*** Variables ***
${APP_URL}


*** Keywords ***
the browser is opened
    open new browser instance

the application is launched
    ${APP_URL}=    launch application
    Set test variable    ${APP_URL}
#    [Return]    ${APP_URL}

the application url is opened
    current url is    ${APP_URL}

the user form is displayed
    browser displays form page

the user form is submitted
    create download button is clicked

a warning message about missing user data is displayed


the download archive is not created
