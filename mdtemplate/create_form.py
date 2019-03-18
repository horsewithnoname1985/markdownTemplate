"""
This module creates a template for a markup language document and provides the
necessary files to transform it into an HTML document. When launching the module
an HTML form is provided, where the user can make settings for the produced
template. When submitting these, the resulting files are immediately offered as
download as a zip archive file. These contain the following files:
- Markup language template
- CSS file for HTML styling
- Template HTML file
- Script file to start HTML creation (Windows: *.bat, Unix/Linux/OSX: *.sh)
Please note, that pandoc must be installed to create the HTML file (see
https://pandoc.org/)
"""

__version__ = "0.1"

from flask import Flask, render_template, request, send_file, jsonify
from os.path import basename, dirname, abspath
from sys import platform
from shutil import copyfile, rmtree
from pathlib import Path
import zipfile
import os
import io
import logging
import pathlib
import webbrowser
import random
import threading

# HOSTING
# -------
URL = "http://127.0.0.1"
PORT = 0

# PATHS
# -----
# base dir (relative)
# BASE_DIR = Path("./")
# base dir (absolute)
BASE_DIR = Path(dirname(os.path.abspath(__file__)))

# temporary output dir
TEMP_DIR = BASE_DIR.joinpath("temp")
TEMP_IMG_DIR = BASE_DIR.joinpath("temp/img")

# base dir of the templates
TEMPLATES_DIR = BASE_DIR.joinpath("files/templates")

# base dir of add-on files
ADDONS_DIR = BASE_DIR.joinpath("files/addons")

# template sub-directories
STYLESHEET_DIR = TEMPLATES_DIR.joinpath("css")
HTML_DIR = TEMPLATES_DIR.joinpath("html")
MARKDOWN_DIR = TEMPLATES_DIR.joinpath("markdown")
IMG_DIR = TEMPLATES_DIR.joinpath("img")

# SETUP
# -----
# Set this files directory as working dir
os.chdir(dirname(abspath(__file__)))

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = TEMP_DIR

logging.basicConfig(level=logging.INFO,
                    format=" %(asctime)s - %(levelname)s - %(message)s")


def main(autostart=False):
    """Launches app on localhost"""
    global PORT
    PORT = 5000 + random.randint(0, 999)
    url = URL + ":{0}".format(PORT)

    if autostart:
        threading.Timer(1.25, lambda: webbrowser.open(url)).start()
    app.run(port=PORT, debug=False)


@app.route('/')
def form_page():
    return render_template('form.html')


@app.route('/create_template', methods=["POST", "GET"])
def get_template_as_download() -> 'zipfile':
    """Define 'Create template' button click action"""
    reset_temp_dir()
    templatezipfile = create_download_archive()
    return send_file(templatezipfile, as_attachment=True)


@app.route('/shutdown')
def shutdown():
    """Initiates server shutdown"""
    shutdown_server()
    return 'Server shutting down...'


def shutdown_server():
    """Shutting down the flask server - Used for tests teardown only"""
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def check_mandatory_fields():
    pass


def reset_temp_dir():
    """Creates output directory structure for temporary files"""
    if os.path.exists(TEMP_DIR):
        rmtree(TEMP_DIR)

    os.makedirs(TEMP_DIR)
    os.makedirs(TEMP_IMG_DIR)


def copy_to_temp(src, temp_dir: str = ""):
    """Copy any file to temp directory"""
    copyfile(src, TEMP_DIR.joinpath(temp_dir + src.name))
    logging.warning('copied to ' +
                    str(TEMP_DIR.joinpath(temp_dir + src.name)))


def create_download_archive():
    """Triggers creation of template archive"""

    prepare_files()
    output_archive_file = zip_output_files()

    return output_archive_file


def prepare_files():
    """Copies proper template or created files into temp dir"""
    logging.info("Start preparing files ...")

    user_input = get_user_input()

    language = user_input['language']
    author = user_input['author']
    date = user_input['date']
    title = user_input['title']
    project = user_input['project']
    filename = user_input['filename']
    style = user_input['style']

    # Assign template filename (derived from user input)
    html_template_filename = style + "_template_" + language + ".html"
    css_filename = style + ".css"

    # Copy template files to temp dir
    copy_to_temp(ADDONS_DIR.joinpath("md-to-toc.py"))
    copy_to_temp(ADDONS_DIR.joinpath("README.md"))
    copy_to_temp(STYLESHEET_DIR.joinpath(css_filename))
    copy_to_temp(HTML_DIR.joinpath(html_template_filename))
    copy_to_temp(IMG_DIR.joinpath(style + ".png"), 'img/')

    # Create additional files inside temp dir
    markdown_filename = prepare_markdown_file(author, title, date, project,
                                              language, filename)
    prepare_script_files(markdown_filename, html_template_filename,
                         css_filename)

    logging.info("Prepared all files.")


def prepare_script_files(markdown_file: str, template_file: str,
                         style_filename: str) -> None:
    """Creates html creation script files inside temp directory"""
    logging.info("Preparing script files ...")

    # Paths definition
    batch_script_path = Path(TEMP_DIR.joinpath("make_html.bat"))
    shell_script_path = Path(TEMP_DIR.joinpath("make_html.sh"))

    # Creating and writing into files
    try:
        with batch_script_path.open(mode="w") as bash_script:
            print("@echo off", file=bash_script)
            print("pandoc -f markdown --template=" + template_file
                  + " --css " + style_filename + " -t html " + "\""
                  + markdown_file + "\"" + " -o " + "\""
                  + markdown_file.rstrip(".markdown") + ".html"
                  + "\"", file=bash_script)

        with shell_script_path.open(mode="w") as shell_script:
            print("#!/bin/bash", file=shell_script)
            print("cd \"$(dirname \"$0\")\"", file=shell_script)
            print("pandoc -f markdown --template=" + template_file
                  + " --css " + style_filename + " -t html " + "\""
                  + markdown_file + "\"" + " -o " + "\""
                  + markdown_file.rstrip(".markdown")
                  + ".html" + "\"", file=shell_script)

    except OSError:
        logging.error("Cannot create script files.")

    logging.info("Prepared script files.")


def zip_output_files() -> zipfile.ZipFile:
    """Creates archive files of temp directory content"""
    archive_file = None

    # Define archive filename based on user input
    filename = request.form['filename']
    archive_filepath = TEMP_DIR.joinpath(filename + "_template_files.zip")

    logging.info("Archiving files ...")

    files = get_prepared_files_as_list()

    # Create archive file depending on user system
    try:
        if platform == "linux":
            archive_file = zipfile.ZipFile(archive_filepath, mode="w",
                                           compression=zipfile.ZIP_BZIP2)

        elif platform == "darwin":
            archive_file = zipfile.ZipFile(archive_filepath, mode="w",
                                           compression=zipfile.ZIP_DEFLATED)

        elif platform == "win32":
            archive_file = zipfile.ZipFile(archive_filepath, mode="w")

        for file in files:
            source = pathlib.Path(file)
            destination = pathlib.Path(*source.parts[1:])
            archive_file.write(source, destination)

        archive_file.close()

    except RuntimeError:
        logging.error("Unable to create archive file!")

    logging.info("Created archive file.")

    return archive_file.filename


def get_prepared_files_as_list() -> list:
    """Returns temp dir content as a list of filepaths"""
    all_files = []

    for root, directories, filenames in os.walk(TEMP_DIR):
        for directory in directories:
            all_files.append(os.path.join(root, directory))
        for filename in filenames:
            all_files.append(os.path.join(root, filename))

    return all_files


def get_user_input() -> dict:
    user_input = dict()
    user_input['language'] = request.form['language']
    user_input['author'] = request.form['author']
    user_input['date'] = request.form['date']
    user_input['title'] = request.form['title']
    user_input['project'] = request.form['project']
    user_input['filename'] = request.form['filename']
    user_input['style'] = request.form['style']

    return user_input


def prepare_markdown_file(author, title, date, project, language, filename):
    """Creates markdown template file based on user input inside temp dir"""
    template = None

    logging.info("Preparing markdown template file...")

    # Creating and writing into markdown template file
    try:
        template = io.open(TEMP_DIR.joinpath(filename + "_v1.0.markdown"),
                           mode="w",
                           encoding="utf-8")
        template.write("---" + "\n")
        template.write("author: " + author + "\n")
        template.write("project: " + project + "\n")
        template.write("title: " + title + "\n")
        template.write("date: " + date + "\n")
        template.write("version: 1.0" + "\n")
        template.write("---" + "\n")

        introduction_str = "Introduction"
        considerations_str = "Preliminary considerations"
        test_setup_str = "Test setup and execution"
        results_str = "Results"
        conclusion_str = "Conclusion"

        if language == 'lang_de':
            introduction_str = "Einleitung"
            considerations_str = "Vorüberlegungen"
            test_setup_str = "Testaufbau und -durchführung"
            results_str = "Testergebnisse"
            conclusion_str = "Fazit"

        template.write("## " + introduction_str + "\n")
        template.write("\n")
        template.write("## " + considerations_str + "\n")
        template.write("\n")
        template.write("## " + test_setup_str + "\n")
        template.write("\n")
        template.write("## " + results_str + "\n")
        template.write("\n")
        template.write("## " + conclusion_str + "\n")
        template.write("\n")

        template.close()

        logging.info("Prepared markdown template file")

    except IOError:
        logging.error("Unable to prepare markdown template file")

    return basename(template.name)
