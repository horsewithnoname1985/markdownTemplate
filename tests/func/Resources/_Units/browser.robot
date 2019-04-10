*** Settings ***
Documentation   Browser action and verification check keywords
Resource        ${EXECDIR}/Resources/_LibraryAdapters/SeleniumLibraryAdapter.robot


*** Keywords ***
open new browser instance
    open browser    url=about:blank

the browser is closed
    close all browsers

application url is opened
    [Arguments]    ${APP_URL}
    open browser  url=${APP_URL}  browser=firefox

verify current url
    [Arguments]    ${URL}
    location should be    ${URL}

the user form is displayed
    page should contain  Welcome to the markdown template creation!