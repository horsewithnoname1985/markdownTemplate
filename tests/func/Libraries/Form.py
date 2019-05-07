# from configparser import ConfigParser
# from pathlib import Path
# from os.path import dirname
# import os
# from tests.func.Libraries.helper.decorators import checkargs
from tests.func.Libraries.helper.config_files import get_ini_section_data
from tests.func.Libraries.helper.config_files import combine_dict_values
# from tests.func.Libraries.helper.selenium_helper import SeleniumHelper
from mdtemplate.mdtemplate import form_field_names
from robot.api.deco import keyword
# from SeleniumLibrary import SeleniumLibrary
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger

# class Form(SeleniumLibrary):
class Form:

    selenium_lib = BuiltIn().get_library_instance('SeleniumLibrary')
    locator_section = 'css'
    input_data_section = 'default'
    # locators = get_ini_section_data("../tests/func/Resources/_Variables/locators.ini",
    #                                 locator_section)
    # input_data = get_ini_section_data("../tests/func/Resources/_Variables/test_data.ini",
    #                                   input_data_section)

    @keyword("fill out form using proper data")
    def insert_all_form_data(self):
        self.insert_all_but_form_data()

    @keyword("fill out form except ${exclude}")
    def insert_all_but_form_data(self, exclude=None) -> None:
        """Puts data into the mdtemplate user form

        :param exclude:
        :return: None
        """

        locators = get_ini_section_data(
            "../tests/func/Resources/_Variables/locators.ini",
            self.locator_section)
        input_data = get_ini_section_data(
            "../tests/func/Resources/_Variables/test_data.ini",
            self.input_data_section)

        actions = self._get_actions(locators, input_data, exclude)

        for locator, input_value in actions.items():

            element = self.selenium_lib.driver.find_element_by_css_selector(
                locator)
            element_type = self._get_element_type(element)

            if element_type in ["text", "textarea", "date"]:
                element.send_keys(input_value)

            elif element_type == "radio" and input_value == "yes":
                element.click()

    @keyword
    def get_form_data_for_post_request(self) -> dict:
        """Prepares input data to be processed within a POST request

        :return: post_data
        :rtype: dict
        """

        # input_data = get_ini_section_data(self.paths['test_data'], 'default')

        post_data = {}
        for name, input_value in self.input_data.items():
            if name in form_field_names:
                post_data[name] = self._process_for_post_data(input_value)

        return post_data

    def _process_for_post_data(self, value: str) -> str:
        value = value.replace(" ", "+")
        # value = value.encode("utf-8")
        return value

    def _get_element_type(self, element) -> str:
        """Returns element type as string

        text ... text field
        radio ... radio button
        :param element: WebElement
        :rtype: str
        """

        element_type = element.get_attribute("type")
        if not type:
            if element.get_attribute("cols") and element.get_attribute("rows"):
                element_type = "radio"

        return element_type

    def _get_actions(self,
                     locators: dict,
                     input_data: dict,
                     exclude: str = None) -> dict:
        # css_locators = get_ini_section_data(self.paths['locators'], 'css')
        # input_data = get_ini_section_data(self.paths['test_data'], 'default')

        if exclude:
            input_data = self._remove_excluded_input(input_data, exclude)

        input_data = self._transform_test_data_to_match_locators(input_data)
        actions = combine_dict_values(locators, input_data)

        return actions

    def _transform_test_data_to_match_locators(self, data: dict) -> dict:

        for name, value in data.items():
            if name == "language":
                data.pop(name)
                if value.lower() == "en":
                    data["lang_en"] = True
                elif name.lower() == "de":
                    data["lang_de"] = True
            if name == "style":
                data.pop(name)
                if value.lower() == "default":
                    data["style_default"] = True
                if value.lower() == "robot":
                    data["style_robot_framework"] = True

        return data

    def _remove_excluded_input(self, input_data: dict, exclude: str) -> dict:
        for key in input_data.keys():
            if key.lower() == exclude.lower():
                input_data.pop(key)

        return input_data


if __name__ == '__main__':
    f = Form()
    f.insert_all_form_data()
