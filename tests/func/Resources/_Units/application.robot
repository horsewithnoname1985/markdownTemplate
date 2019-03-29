*** Settings ***
Documentation   Application action keywords
Resource        ${EXECDIR}/func/Resources/_LibraryAdapters/SeleniumLibraryAdapter.robot
Resource        ${EXECDIR}/func/Resources/_LibraryAdapters/ApplicationLibraryAdapter.robot
#Library             app_runner.Application


*** Keywords ***
launch application
    ${APP_URL}=   launch application
    Set test variable  ${APP_URL}
    [Return]    ${APP_URL}

the application is closed
    shutdown application