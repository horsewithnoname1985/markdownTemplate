#! python3
from bs4 import BeautifulSoup
import ssl
from urllib.request import urlopen
import json
import re


file = open("content.txt", "a")
i = 1

url = "https://www.gog.com/games?sort=title&page=1"

context = ssl._create_unverified_context()
content = urlopen(url, context=context).read()

soup = BeautifulSoup(content, "html.parser")
data = soup.find('script', type='text/javascript').string

data_regex = re.compile(r'var .* = ')
data = re.split(data_regex, data)

mydata = data[1].replace("};", "}")

my_json_data = json.loads(mydata)

for i in range (49):
    file.write(my_json_data['products'][i]['title'] + "\n")



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
