*** Settings ***
Documentation   Creation of new template files

Resource        ${EXECDIR}/Resources/_Units/form.robot


*** Keywords ***
the template archive file is created
    [Documentation]     Check output temp dir if correct archive file exists
    [Arguments]         ${form_filename}
    file should exist   ${SRC_DIR}/${form_filename}_template_files.zip

the download archive is not created
    Log  Implement me
    #TODO: Implement keyword

template files are not created
    [Documentation]     Check output temp dir is empty or does not exist
    file should not exist   ${SRC_DIR}/*_template_files.zip

#the download archive is not created
the archive file is not created
    Log  Implement me
    #TODO: Implement keyword

the archive file is offered for download
    Log  Implement me
    # TODO: Implement keyword

all template files reside in the resulting archive
    Log  Implement me
    # TODO: Implement keyword
    # all templates files

the selected files reside in the resulting archive
    Log  Implement me
    # TODO: Implement keyword
    # css + html template

the resulting script files reference the correct template files
    Log  Implement me
    # TODO: Implement keyword

the resulting markdown file contains the correct content
    Log  Implement me
    # TODO: Implement keyword
