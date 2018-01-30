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

from flask import Flask, render_template, request, send_from_directory
from os.path import basename
import zipfile
import os

app = Flask(__name__, static_folder="/")


@app.route('/')
def form_page() -> 'html':
    return render_template('form.html')


@app.route('/create_template', methods=['POST'])
def create_template():
    language = request.form['language']
    author = request.form['author']
    date = request.form['date']
    title = request.form['title']
    project = request.form['project']

    stylesheet_dir = "files/E+L_style.css"
    el_template = "files/el_template_en.html"
    markdown_templ = str(create_markdown_file(author, title, date,
                                              project, language))

    if language == 'DE':
        el_template = "files/el_template_de.html"

    files = [el_template, markdown_templ, stylesheet_dir]

    zip_template_files("el_markdown_template_files.zip", files)
    os.remove(markdown_templ)

    return render_template("download_ready.html")


@app.route('/el_markdown_template_files.zip', methods=['GET'])
def download():
    return send_from_directory(directory="",
                               filename="el_markdown_template_files.zip",
                               as_attachment=False, mimetype="application/zip")
# TODO: Find a way to delete the *.zip file after download


def zip_template_files(archive_file, files) -> 'zip_file':
    myfile = zipfile.ZipFile(archive_file, "w", )
    for file in files:
        myfile.write(file, basename(file))
    myfile.close()


def create_markdown_file(author, title, date, project, language):
    template = open("files/" + title + "_v1.0.markdown", "w")
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

    if language == 'DE':
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

# TODO: Create a function that creates script files and add these to zip file


app.run(debug=True)
