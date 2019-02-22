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
[virtual environment](some_link) (here, we name it `myscripts`)

    $ virtualenv -p /usr/bin/python3 ~/.virtualenv/myscripts
    
Activate the environment via
    
    $ source ~/.virtualenv/myscripts/bin/activate
    
or on Windows:

    C:\Users\<yourusername>\.virtualenvs\myscripts\Scripts\activate

then install via pip::

    (script)$ pip install mdemplate

# Usage
Run the script from within your python virtual environment

    (script)$ mdtemplate
    
The web browser, containing the template form is launched automatically.    

Alternatively, the script can be executed from the shell without 
activating your virtual environment by placing a reference to the script 
executable inside a sourced directory folder (e.g. `/usr/bin` or `~/bin`).

    $ sudo ln -s ~/.virtualenv/myscripts/bin/mdtemplate /usr/bin
    
or on Windows (cmd.exe must be opened as administrator)

    mklink C:\bin\mdtemplate.exe C:\Users\<yourusername>\.virtualenvs\myscripts\Scripts\mdtemplate.exe
    
Now you can run the script via
    
    $ mdtemplate
