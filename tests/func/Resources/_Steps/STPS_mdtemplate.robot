*** Settings ***
Documentation       Suite description
Library             SeleniumLibrary
Library             app_runner.Application


*** Keywords ***
the browser is closed
    close all browsers

the application is launched
    ${APP_URL}=   launch application
    Set test variable  ${APP_URL}

the application url is opened
    open browser  url=${APP_URL}  browser=firefox

the user form is displayed
    page should contain  Welcome to the markdown template creation!