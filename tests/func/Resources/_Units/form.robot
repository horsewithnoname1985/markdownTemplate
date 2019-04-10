*** Settings ***
Documentation       User form interaction keywords
Resource            ${EXECDIR}/Resources/_LibraryAdapters/SeleniumLibraryAdapter.robot
Resource            ${EXECDIR}/Resources/_LibraryAdapters/RequestsLibraryAdapter.robot
Resource            ${EXECDIR}/Resources/_LibraryAdapters/FormLibraryAdapter.robot

*** Variables ***
${FLD_TITLE_CSS}            css:#title_field
${FLD_AUTHOR_CSS}           css:#author_field
${FLD_DATE_CSS}             css:#date_selector
${FLD_PROJECT_CSS}          css:#project_field
${FLD_FILENAME_CSS}         css:#filename_field

${RADIO_LANGUAGE_DE_CSS}        css:#lang_de
${RADIO_LANGUAGE_EN_CSS}        css:#lang_en
${RADIO_TEMPLATE_DEFAULT_CSS}   css:#tmpl_default
${RADIO_TEMPLATE_RF_CSS}        css:#tmpl_robot_framework


*** Keywords ***
the user form is submitted
    # TODO: reimplement keyword
    click button    ${XPATH_CREATE_TEMPLATE_BUTTON}

the download file is not created
    alert should be present    Please fill out all mandatory fields

the entire form except the ${exclude} is filled with valid data
    [Documentation]    A single data set can be excluded from receiving
    ...    proper input data. For radio button, this means, that the
    ...    preselected setting is applied.
    ...    ${exclude} must be the name of a data element (e.g. style, title)
    fill out form except ${exclude}

the entire form is filled with valid data
    fill out form using proper data

send POST request to create template archive
    create session    mdtemplate      ${APP_URL}
    &{header}=    create dictionary   Content-Type=application/x-www-form-urlencoded
    &{data}=    get form data for post request
    ${resp}=          Post request    mdtemplate    /create_template_archive
    ...    data=&{data}    headers=&{header}
    [Return]    ${resp}

a warning message about missing user data is displayed
    Log  Implement me
    # TODO: Implement keyword

the ${language} language is selected
    Log  Implement me
    # TODO: Implement keyword

the ${style} style template is selected
    Log  Implement me
    # TODO: Implement keyword
