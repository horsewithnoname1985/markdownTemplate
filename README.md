# Create report - Usage

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
