from mdtemplate import create_form
from threading import Thread
import time


def get_url():
    return create_form.URL + ":" + str(create_form.PORT)


def launch_application():
    thread = Thread(target=create_form.main)
    thread.start()
    time.sleep(2)
    url = get_url()

    return get_url()


if __name__ == "__main__":
    flask_thread = Thread(target=create_form.main)
    flask_thread.start()
    time.sleep(2)
    url = get_url()
    print(url)
