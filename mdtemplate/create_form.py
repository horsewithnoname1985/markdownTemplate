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

from flask import Flask, render_template, request, send_file
from os.path import basename, dirname, abspath
from sys import platform
from shutil import copyfile, rmtree
import zipfile
import os
import io
import logging
import pathlib


OUTPUT_DIR = "output/"
FILES_DIR = "files/"
TEMP_DIR = "temp/"
TEMP_IMG_DIR = "temp/img/"

STYLESHEET_DIR = "files/templates/css/"
HTML_DIR = "files/templates/html/"
MARKDOWN_DIR = "files/templates/markdown/"
IMG_DIR = "files/templates/img/"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = OUTPUT_DIR
os.chdir(dirname(abspath(__file__)))

logging.basicConfig(level=logging.INFO,
                    format=" %(asctime)s - %(levelname)s - %(message)s")


def main():
    pass


@app.route('/')
def form_page():
    return render_template('form.html')


@app.route('/create_template', methods=['POST', "GET"])
def get_template_as_download() -> 'zipfile':
    create_output_dirs()

    templatezipfile = create_download_archive()
    return send_file(templatezipfile, as_attachment=True)


def create_output_dirs():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
        os.makedirs(TEMP_IMG_DIR)


def create_download_archive():
    rmtree(OUTPUT_DIR)

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    prepare_files()

    filename = request.form['filename']
    zip_filename = OUTPUT_DIR + filename + "_template_files.zip"

    output_archive_file = zip_output_files(zip_filename)
    rmtree(TEMP_DIR)

    return output_archive_file


def prepare_files():
    logging.info("Start preparing files ...")

    language = request.form['language']
    author = request.form['author']
    date = request.form['date']
    title = request.form['title']
    project = request.form['project']
    filename = request.form['filename']
    style = request.form['style']

    html_template_filename = style + "_template_" + language + ".html"
    css_filename = style + ".css"

    logging.warning("Current dir: " + os.getcwd())

    copyfile(FILES_DIR + "md-to-toc.py", TEMP_DIR + "md-to-toc.py")
    copyfile(FILES_DIR + "README.md", TEMP_DIR + "README.md")
    copyfile(STYLESHEET_DIR + css_filename, TEMP_DIR + css_filename)
    copyfile(HTML_DIR + style + "_template_" + language + ".html",
             TEMP_DIR + style + "_template_" + language + ".html")
    copyfile(IMG_DIR + style + ".png", TEMP_IMG_DIR + style + ".png")

    markdown_filename = prepare_markdown_file(author, title, date, project,
                                              language, filename)
    prepare_script_files(markdown_filename, html_template_filename,
                         css_filename)

    logging.info("Prepared all files.")


def prepare_script_files(markdown_file, template_file, style_filename):
    logging.info("Preparing script files ...")

    try:
        with open(TEMP_DIR + "make_html" + ".bat", "w") as bash_script:
            print("@echo off", file=bash_script)
            print("pandoc -f markdown --template=" + template_file
                  + " --css " + style_filename + " -t html " + "\"" + markdown_file +
                  "\"" + " -o " + "\"" + markdown_file.rstrip(".markdown") +
                  ".html" + "\"", file=bash_script)

        with open(TEMP_DIR + "make_html" + ".sh", "w") as shell_script:
            print("#!/bin/bash", file=shell_script)
            print("cd \"$(dirname \"$0\")\"", file=shell_script)
            print("pandoc -f markdown --template=" + template_file
                  + " --css " + style_filename + " -t html " + "\"" + markdown_file +
                  "\"" + " -o " + "\"" + markdown_file.rstrip(".markdown") +
                  ".html" + "\"", file=shell_script)

    except OSError:
        logging.error("Cannot create script files.")

    logging.info("Prepared script files.")


def zip_output_files(archive_filepath) -> 'zipfile':
    archive_file = None

    logging.info("Archiving files ...")

    files = get_prepared_files_as_list()

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
    all_files = []

    for root, directories, filenames in os.walk(TEMP_DIR):
        for directory in directories:
            all_files.append(os.path.join(root, directory))
        for filename in filenames:
            all_files.append(os.path.join(root, filename))

    return all_files


def prepare_markdown_file(author, title, date, project, language, filename):
    template = None

    logging.info("Preparing markdown template file...")

    try:
        template = io.open(TEMP_DIR + filename + "_v1.0.markdown", mode="w",
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


app.run(debug=True)
