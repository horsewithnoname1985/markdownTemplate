# Prerequisites
Converting the markdown document into an HTML file requires 
[pandoc](https://www.pandoc.org/installing.html) to be installed.

## For styles
The **Robot Framework** style requires the OCR-A font to be installed.
It is pre-installed on Windows systems, but on Linux and OSX systems it
must be installed manually.
You can download it [here](https://www.wfonts.com/font/ocr-a)
(add OCR-A.ttf to your system's fonts).

# Installation
It is recommended to install the package within a 
[virtual environment](some_link)

    $ virtualenv -p /usr/bin/python3 ~/.virtualenv/scripts_venv
    
Activate the environment via
    
    $ source ~/.virtualenv/scripts/bin/activate

then install via pip::

    (script)$ pip install mdemplate

# Usage
Run the script from within your python virtual environment

    (script)$ mdtemplate
    
The web browser, containing the template form is lauched automatically.    

Alternatively, the script can be executed without activating your
virtual environment. Copy the executable from your environment's 
`bin` directory to a your `/usr/bin` directory

    $ sudo cp ~/.virtualenv/scripts/bin/mdtemplate /usr/bin
    
Now you can run the script via
    
    $ mdtemplate

Another method is to create an link

**Windows**

Default host address is *http://127.0.0.1:5000/*
``` batch
@echo off
cd C:\your\path\to\markdownTemplate-master\create_report
"C:\your\path\to\python\interpreter\Scripts\python" create_form.py %*
start "" http://127.0.0.1:5000/
pause
```
2. Open browser and go to specified address
