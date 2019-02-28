from robot.libraries.BuiltIn import BuiltIn


class SeleniumHelper:

    selenium_lib = BuiltIn().get_library_instance('SeleniumLibrary')

    def get_webdriver_instance(self):
        return self.selenium_lib.driver
