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



1. Create startscript to launch the server

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
