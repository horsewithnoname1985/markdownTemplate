from mdtemplate import mdtemplate
from threading import Thread, Event
from SeleniumLibrary.base import keyword
from tests.func.Libraries.helper.selenium_helper import SeleniumHelper
import time


class Application:
    """
    This class provides keywords for controlling the application under test,
    such as launching and quitting.
    """

    url = ""
    app_thread = None

    def __init__(self):
        self.selenium_helper = SeleniumHelper()

    @staticmethod
    def get_url():
        """Returns current session's application url"""
        return mdtemplate.URL + ":" + str(mdtemplate.PORT)

    @keyword
    def launch_application(self):
        """Hosts app_unused on server"""
        self.app_thread = Thread(target=mdtemplate.main,
                                 args=(False, False, True,))
        self.app_thread.start()
        time.sleep(2)
        self.url = self.get_url()
        return self.url

    @keyword()
    def shutdown_application(self):
        """Shuts down application server"""
        driver = self.selenium_helper.get_webdriver_instance()
        driver.get(self.url + '/shutdown')


class ApplicationThread(Thread):
    """Flask application thread which provides stop method"""
    def __init__(self):
        super(ApplicationThread, self).__init__()
        self._stop_event = Event()

    def stop(self):
        self._stop_event.set()
