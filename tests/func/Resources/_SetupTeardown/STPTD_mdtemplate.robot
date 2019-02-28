*** Settings ***
Documentation   Suite description
Resource        ../_Steps/STPS_mdtemplate.robot
Library         ../../Libraries/app_runner.py
Library         SeleniumLibrary


*** Keywords ***
Start app and open url
    the browser is closed
    the application is launched
    the application url is opened

Close browser and app
    shutdown application
    close browser
