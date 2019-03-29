"""
This module creates a template for a markup language document and provides the
necessary files to transform it into an HTML document. When launching the
module an HTML form is provided, where the user can make settings for the
produced template. When submitting these, the resulting files are immediately
offered as download as a zip archive file. These contain the following files:
- Markup language template
- CSS file for HTML styling
- Template HTML file
- Script file to start HTML creation (Windows: *.bat, Unix/Linux/OSX: *.sh)
Please note, that pandoc must be installed to create the HTML file (see
https://pandoc.org/)
"""

__version__ = "0.1"

from flask import Flask, render_template, request, send_file
from os.path import dirname, abspath
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
from abc import ABC
from configparser import ConfigParser

# HOSTING
# -------
URL = "http://127.0.0.1"
PORT = 0

# PATHS
# -----
# base dir (relative)
BASE_DIR = Path("./")

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
app.config["UPLOAD_FOLDER"] = TEMP_DIR

logging.basicConfig(
    level=logging.INFO, format=" %(asctime)s - %(levelname)s - %(message)s"
)

config_parser = ConfigParser()
config_parser.read("form_field_names.ini")

form_field_names = dict(config_parser.items(config_parser.sections()[0]))


def main(autostart=False):
    """Launches app on localhost"""
    global PORT
    PORT = 5000 + random.randint(0, 999)
    url = URL + ":{0}".format(PORT)

    if autostart:
        threading.Timer(1.25, lambda: webbrowser.open(url)).start()
    app.run(port=PORT, debug=False)


@app.context_processor
def inject_form_field_names():
    return form_field_names


@app.route("/")
def form_page():
    return render_template("form.html")


@app.route("/create_template", methods=["POST", "GET"])
def get_template_as_download() -> zipfile:
    """Define 'Create template' button click action"""

    user_data = UserInputData()
    archiver = TemplateArchiver(user_data)

    return send_file(archiver.template_archive, as_attachment=True)


@app.route("/shutdown")
def shutdown():
    """Initiates server shutdown"""
    shutdown_server()
    return "Server shutting down..."


def shutdown_server():
    """Shutting down the flask server - Used for tests teardown only"""
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()


class UserInputData:
    """Contains user input data"""

    data = {}

    def __init__(self):
        self.language = request.form[form_field_names["language"]]
        self.author = request.form[form_field_names["author"]]
        self.project = request.form[form_field_names["project"]]
        self.date = request.form[form_field_names["date"]]
        self.title = request.form[form_field_names["title"]]
        self.style = request.form[form_field_names["style"]]
        self.filename = request.form[form_field_names["filename"]]


class TemplateArchiver:
    """Gathers all files in order to create an downloadable archive"""

    def __init__(self, user_input: UserInputData):

        self.user_input = user_input
        self._reset_temp_dir()

        # Create required template files
        self.html_template = HTMLTemplateFile(user_input)
        self.logo = LogoImageFile(user_input)
        self.css = StylesheetFile(user_input)
        self.markdown_template = MarkdownTemplate(user_input)
        self.bash_script = MarkdownToHTMLScript(
            script_type="batch",
            html_template_filename=self.html_template.path.name,
            css_filename=self.css.path.name,
            markdown_template_filename=self.markdown_template.path.name,
        )
        self.bash_script = MarkdownToHTMLScript(
            script_type="shell",
            html_template_filename=self.html_template.path.name,
            css_filename=self.css.path.name,
            markdown_template_filename=self.markdown_template.path.name,
        )
        self.md_to_toc = MarkdownToTableOfContentsFile()
        self.md_to_toc_readme = MarkdownToTableOfContentsReadmeFile()

        self.template_files = self._get_template_files_as_list()
        self.template_archive = self.zip_template_files()

    @staticmethod
    def _reset_temp_dir():
        """Creates output directory structure for temporary files"""
        if os.path.exists(TEMP_DIR):
            rmtree(TEMP_DIR)

        os.makedirs(TEMP_DIR)
        os.makedirs(TEMP_IMG_DIR)

    @staticmethod
    def _get_template_files_as_list() -> list:
        """Returns temp dir content as a list of filepaths"""

        template_files = []

        for root, directories, filenames in os.walk(TEMP_DIR):
            for directory in directories:
                template_files.append(os.path.join(root, directory))
            for filename in filenames:
                template_files.append(os.path.join(root, filename))

        return template_files

    def zip_template_files(self) -> zipfile:
        """Create archive file from all files in temp directory"""
        archive_file = None

        # Define archive filename based on user input
        archive_filepath = TEMP_DIR.joinpath(
            self.user_input.filename + "_template_files.zip"
        )

        logging.info("Archiving files ...")

        # Create archive file depending on user system
        try:
            if platform == "linux":
                archive_file = zipfile.ZipFile(
                    archive_filepath, mode="w",
                    compression=zipfile.ZIP_BZIP2
                )

            elif platform == "darwin":
                archive_file = zipfile.ZipFile(
                    archive_filepath, mode="w",
                    compression=zipfile.ZIP_DEFLATED
                )

            elif platform == "win32":
                archive_file = zipfile.ZipFile(archive_filepath, mode="w")

            for file in self.template_files:
                source = pathlib.Path(file)
                destination = pathlib.Path(*source.parts[1:])
                archive_file.write(source, destination)

            archive_file.close()

        except RuntimeError:
            logging.error("Unable to create archive file!")

        logging.info("Created archive file.")

        return archive_file.filename


class PredefinedTemplateFile(ABC):
    path = None
    filename = None

    def __init__(self, source_dir: Path, dest_dir: Path):
        self.path = source_dir.joinpath(self.filename)
        self.copy_to_temp(
            source=self.path, destination=dest_dir.joinpath(self.filename)
        )

    @staticmethod
    def copy_to_temp(source: Path, destination: Path):
        copyfile(str(source), str(destination))


class MarkdownToTableOfContentsFile(PredefinedTemplateFile):
    def __init__(self):
        self.filename = "md-to-toc.py"
        super(MarkdownToTableOfContentsFile, self).__init__(
            source_dir=ADDONS_DIR, dest_dir=TEMP_DIR
        )


class MarkdownToTableOfContentsReadmeFile(PredefinedTemplateFile):
    def __init__(self):
        self.filename = "README.md"
        super(MarkdownToTableOfContentsReadmeFile, self).__init__(
            source_dir=ADDONS_DIR, dest_dir=TEMP_DIR
        )


class HTMLTemplateFile(PredefinedTemplateFile):
    """HTML template file which defines the output HTML structure"""

    def __init__(self, user_input: UserInputData):
        self.filename = user_input.style + "_template_" \
                        + user_input.language + ".html"
        super(HTMLTemplateFile, self).__init__(
            source_dir=HTML_DIR,
            dest_dir=TEMP_DIR)


class LogoImageFile(PredefinedTemplateFile):
    """Logo image file that is displayed in the output HTML"""

    def __init__(self, user_input: UserInputData):
        self.filename = user_input.style + ".png"
        super(LogoImageFile, self).__init__(
            source_dir=IMG_DIR,
            dest_dir=TEMP_IMG_DIR)


class StylesheetFile(PredefinedTemplateFile):
    """Stylesheet file for HTML output"""

    def __init__(self, user_input: UserInputData):
        self.filename = user_input.style + ".css"
        super(StylesheetFile, self).__init__(
            source_dir=STYLESHEET_DIR,
            dest_dir=TEMP_DIR
        )


class MarkdownToHTMLScript:
    """Script file which creates an HTML file from a markdown document"""

    def __init__(
            self,
            script_type: str,
            html_template_filename: str,
            css_filename: str,
            markdown_template_filename: str,
    ):
        self.html_template_filename = html_template_filename
        self.css_filename = css_filename
        self.markdown_template_filename = markdown_template_filename
        if script_type == "shell":
            self._create_shell_script_file()
        elif script_type == "batch":
            self._create_batch_script_file()
        else:
            logging.error("Please provide proper script type")

    def _create_shell_script_file(self):
        self.path = Path(TEMP_DIR.joinpath("make_html.sh"))
        try:
            with self.path.open(mode="w") as shell_script:
                print("#!/bin/bash", file=shell_script)
                print('cd "$(dirname "$0")"', file=shell_script)
                print(
                    "pandoc -f markdown --template="
                    + self.html_template_filename
                    + " --css "
                    + self.css_filename
                    + " -t html "
                    + '"'
                    + self.markdown_template_filename
                    + '"'
                    + " -o "
                    + '"'
                    + self.markdown_template_filename
                    .rstrip("markdown")
                    .rstrip(".")
                    + ".html"
                    + '"',
                    file=shell_script,
                )
        except OSError:
            logging.error("Cannot create script files.")

    def _create_batch_script_file(self):
        self.path = Path(TEMP_DIR.joinpath("make_html.bat"))

        try:
            with self.path.open(mode="w") as bash_script:
                print("@echo off", file=bash_script)
                print(
                    "pandoc -f markdown --template="
                    + self.html_template_filename
                    + " --css "
                    + self.css_filename
                    + " -t html "
                    + '"'
                    + self.markdown_template_filename
                    + '"'
                    + " -o "
                    + '"'
                    + self.markdown_template_filename
                    .rstrip("markdown")
                    .rstrip(".")
                    + ".html"
                    + '"',
                    file=bash_script,
                )

        except OSError:
            logging.error("Cannot create script files.")


class MarkdownTemplate:
    """Initial markdown template used for further editing"""

    def __init__(self, user_input: UserInputData):
        self.path = STYLESHEET_DIR.joinpath(user_input.filename + ".markdown")
        self.user_input = user_input
        self._create_markdown_file()

    def _create_markdown_file(self):
        try:
            template = io.open(
                TEMP_DIR.joinpath(self.user_input.filename + ".markdown"),
                mode="w",
                encoding="utf-8",
            )
            template.write("---" + "\n")
            template.write("author: " + self.user_input.author + "\n")
            template.write("project: " + self.user_input.project + "\n")
            template.write("title: " + self.user_input.title + "\n")
            template.write("date: " + self.user_input.date + "\n")
            template.write("version: 1.0" + "\n")
            template.write("---" + "\n")

            introduction_str = "Introduction"
            considerations_str = "Preliminary considerations"
            test_setup_str = "Test setup and execution"
            results_str = "Results"
            conclusion_str = "Conclusion"

            if self.user_input.language == "lang_de":
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
