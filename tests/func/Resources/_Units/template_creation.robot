*** Settings ***
Documentation   Creation of new template files

Resource        ${EXECDIR}/Resources/_Units/form.robot


*** Keywords ***
template archive file is created
    [Documentation]     Check output temp dir if correct archive file exists
    [Arguments]         ${form_filename}
    file should exist   ${SRC_DIR}/${form_filename}_template_files.zip

template files are not created
    [Documentation]     Check output temp dir is empty or does not exist
    file should not exist   ${SRC_DIR}/*_template_files.zip