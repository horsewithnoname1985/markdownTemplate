*** Settings ***
Documentation       User form interaction keywords
Resource            ${EXECDIR}/func/Resources/_LibraryAdapters/SeleniumLibraryAdapter.robot
Resource            ${EXECDIR}/func/Resources/_Data/form_data.robot

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
create download button is clicked
    click button    ${XPATH_CREATE_TEMPLATE_BUTTON}

the download file is not created
    alert should be present    Please fill out all mandatory fields

all fields receive proper data
    input text      ${FLD_TITLE_CSS}                ${FORM_DATA_TITLE}
    input text      ${FLD_AUTHOR_CSS}               ${FORM_DATA_AUTHOR}
    input text      ${FLD_DATE_CSS}                 ${FORM_DATA_DATE}
    input text      ${FLD_PROJECT_CSS}              ${FORM_DATA_PROJECT}
    click element   ${RADIO_LANGUAGE_DE_CSS}
    input text      ${FLD_FILENAME_CSS}             ${FORM_DATA_FILENAME}
    click element   ${RADIO_TEMPLATE_DEFAULT_CSS}

