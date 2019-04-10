#*** Settings ***
#Documentation   user form steps
#
#Resource        ${EXECDIR}/Resources/_Units/form.robot
##Resource        ${EXECDIR}/Resources/_Units/application.robot
#Resource        ${EXECDIR}/Resources/_Units/browser.robot
##Resource        ${EXECDIR}/Resources/_Units/template_archive.robot
#
#
#*** Keywords ***
#the user form is displayed
#    browser displays form page
#
#the entire form is filled with valid data
#    all fields receive proper data
#
#the entire form except the ${exclude} is filled with valid data
#    # TODO: Implement keyword
#
#the user form is submitted
#    ${SUBMIT_RESPONSE}=    send POST request to create template archive
#    Set test variable   ${SUBMIT_RESPONSE}
#
#the download archive is not created
#    # TODO: Implement keyword
#    # check if <filename>_template_files.zip resides in /temp
#
#the archive file is offered for download
#    should be equal as strings      ${SUBMIT_RESPONSE.status_code}     200
#
#a warning message about missing user data is displayed
#    # TODO: Implement keyword
