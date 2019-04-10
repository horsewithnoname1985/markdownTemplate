*** Settings ***
#Documentation   Application action keywords
Resource        ${EXECDIR}/Resources/_Units/browser.robot
Resource        ${EXECDIR}/Resources/_LibraryAdapters/SeleniumLibraryAdapter.robot


*** Keywords ***
the application is launched
    [Documentation]   Similar to setup method, but without opening browser

    ${APP_URL}=    application.launch application
    Set test variable    ${APP_URL}

the application url is opened
    [Documentation]  Opens application url (app must be launched priorly)

    open browser  url=${APP_URL}  browser=firefox

#the user form is displayed
#    browser displays form page