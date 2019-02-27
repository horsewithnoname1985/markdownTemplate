from mdtemplate import create_form
from threading import Thread
import time


def get_url(result):
    result['url'] = create_form.URL + ":" + create_form.PORT
    return url


def launch_application():

    thread = Thread(target=create_form.main)
    thread.start()
    time.sleep(2)


if __name__ == "__main__":
    launch_application()
    result = []
    thread = Thread(target=get_url, args=(result, 1))
    thread.start()
    url = str(result[1])
    print(result[1])

