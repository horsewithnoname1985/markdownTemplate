#! python3
from bs4 import BeautifulSoup
import ssl
from urllib.request import urlopen
import json
import re

file = open("content.txt", "wb")

for i in range(1, 43, 1):

    url = "https://www.gog.com/games?sort=title&page=" + str(i)
    print(url)

    context = ssl._create_unverified_context()
    content = urlopen(url, context=context).read()

    soup = BeautifulSoup(content, "html.parser")
    data = soup.find('script', type='text/javascript').string

    data_regex = re.compile(r'var .* = ')
    data = re.split(data_regex, data)

    mydata = data[1].replace("};", "}")

    my_json_data = json.loads(mydata)

    for j in range(0, len(my_json_data['products']), 1):
        title = my_json_data['products'][j]['title'].encode("utf-8")
        print(type(title))
        file.write(title + "\n".encode("utf-8"))

    # PROBLEM:
    # The title values are not transmitted via Beatiful Soup because
    # these data is stored in a JavaScript Object. This however, this
    # object somehow does only contain the data for the first site
    # (it must be some kind of template) not the other forty. When
    # running these URLs, the title data is neither inside the html nor
    # inside the JS object.
    # If the site uses the html as template and inputs the data from the JS
    # object, I wonder where it gets the data from, since it is not in the Object.
    # If the JS Object itself is the template, then why don't I get the values
    # from the html?
    # Find out, how this works before continuing!



# TODO: Find a way to extract desired information from a javascript object containing data in json syntax
# The website saves its catalogue content inside json objects.
# Therefore running BeautifulSoup over the page, the information is not
# delivered within the html elements (as seen via inspection in the browser)
# but only within the object, which resides inside a javascript element
# (<script type="text/javascript">JAVA SCRIPT OBJECTS</script>). Inside the script
# element there are three Java Script Objects:
# - gogData
# - translationData
# as well as a gogData.features set. The desired data is within gogData.
#
# see here: https://www.w3schools.com/js/js_json.asp
# Help: https://stackoverflow.com/questions/8049520/web-scraping-javascript-page-with-python
