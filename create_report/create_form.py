"""
This module creates a template for a markup language document and provides the
necessary files to transform it into an HTML document. When launching the module
an HTML form is provided, where the user can make settings for the produced
template. When submitting these, the template is created at a specified direct-
ory. Specifically, the following files are created:
- Markup language template
- CSS file for HTML styling
- Template HTML file
- Script file to start HTML creation (Windows: *.bat, Unix/Linux/OSX: *.sh)
Please note, that pandoc must be installed to create the HTML file (see
https://pandoc.org/)
"""

from flask import Flask, render_template, request, send_file
from os.path import basename
import zipfile
import os

UPLOAD_FOLDER = "output/"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def form_page() -> 'html':
    return render_template('form.html')


def create_template():
    language = request.form['language']
    author = request.form['author']
    date = request.form['date']
    title = request.form['title']
    project = request.form['project']
    filename = request.form['filename']

    print("Language selection" + str(language))

    stylesheet_dir = "files/E+L_style.css"
    el_template = "files/el_template_en.html"
    if language == 'lang_de':
        el_template = "files/el_template_de.html"
    markdown_templ = str(create_markdown_file(author, title, date,
                                              project, language, filename))
    script_files = create_script_files(
        os.path.basename(markdown_templ), os.path.basename(el_template))

    files = [el_template, markdown_templ, stylesheet_dir, script_files[0],
             script_files[1]]

    myfile_outputdir = "output/el_markdown_template_files.zip"
    create_zip_template_files(myfile_outputdir, files)
    os.remove(markdown_templ)

    for file in script_files:
        os.remove(file)

    return myfile_outputdir


@app.route('/create_template', methods=['POST', "GET"])
def create_plus_download():
    templatezipfile = create_template()
    return send_file(templatezipfile, as_attachment=True)


def create_script_files(markdown_file, template_file):
    with open("files/make_html" + ".bat", "w") as bash_script:
        print("@ECHO off", file=bash_script)
        # TODO: Add chiffre for current file's directory
        print("cd to my drive", file=bash_script)
        print("pandoc -f markdown --template=" + template_file
              + " --css E+L_style.css " + "\"" + markdown_file + "\"" + " -o "
              + "\"" + markdown_file.rstrip(".markdown") + ".html" + "\"",
              file=bash_script)

    with open("files/make_html" + ".sh", "w") as shell_script:
        print("#!/bin/bash", file=shell_script)
        print("cd \"$(dirname \"$0\")\"", file=shell_script)
        print("pandoc -f markdown --template=" + template_file
              + " --css E+L_style.css " + "\"" + markdown_file + "\"" + " -o "
              + "\"" + markdown_file.rstrip(".markdown") + ".html" + "\"",
              file=shell_script)

    # script_files = [bash_script, shell_script]

    # shell_script.write("#!/bin/bash\n")
    # shell_script.write("cd \"$(dirname \"$0\")\"\n")
    # shell_script.write(
    #     "pandoc -f markdown --template=" + template_file
    #     + " --css E+L_style.css " + "\"" + markdown_file + "\"" + " -o "
    #     + "\"" + markdown_file.rstrip(".markdown") + ".html" + "\"")
    #
    # bash_script.write("@ECHO off\n")

    # bash_script.write("cd to my drive\n)
    # bash_script.write(
    #     "pandoc -f markdown --template=" + template_file
    #     + " --css E+L_style.css " + "\"" + markdown_file + "\"" + " -o "
    #     + "\"" + markdown_file.rstrip(".markdown") + ".html" + "\"")
    #
    # bash_script.close()
    # shell_script.close()

    return [bash_script.name, shell_script.name]


def create_zip_template_files(archive_file, files) -> 'zip_file':
    myfile = zipfile.ZipFile(archive_file, "w")
    for file in files:
        myfile.write(file, basename(file))
        print(file)
    myfile.close()

    return myfile


def create_markdown_file(author, title, date, project, language, filename):
    template = open("files/" + filename + "_v1.0.markdown", "w")
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

    return template.name


app.run(debug=True)

# ISSUE:
# The false zip file is downloaded after the first initiation of a
# template file (from second one on it is always the first one, except the path
# for the zip file is changed, but then it also only works once
# HYPOTHESIS: The file is created locally (works every time) but is not
# transferred to the host directory, because it already does exist after the
# first creation (Click download: There is already an equally named zip file at
# the called location, so we don't need to take any new one in the local
# directory
#
# 1. SOLUTION:
# Delete the zip file from the host (not the local dir)
# after it has been downloaded
# 2. SOLUTION:
# Create the zip file and start the download within the same
# method. This method is supposed to be called when the 'Submit' button of the
# form is clicked, e.g. the download page is obsolete
# 3. ANOTHER POSSIBLE SOLUTION:
# Make the zip file to be directly stored at the
# host address (not at the local dir) ... don't know, if that's possible

# TODO: Find a way to delete the zip file from the host after being download
# TODO: Put the zip file creation + download into one method -> call on submit
# TODO: Find a way to directly put the zip file in the host output dir
