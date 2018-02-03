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

from flask import Flask, render_template, request, send_file, \
    send_from_directory
from os.path import basename
import zipfile
import os

app = Flask(__name__)


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
    filename = request.form['filename']

    # print(language)
    # print(author)
    # print(date)
    # print(title)
    # print(project)
    # print(filename)

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

    # print(files)

    create_zip_template_files("output/el_markdown_template_files.zip", files)
    os.remove(markdown_templ)

    for file in script_files:
        os.remove(file)

    return render_template("download_ready.html")


@app.route("/get_templates_files")
def download():
    print(os.getcwd())
    # return print("Haha!")
    # return send_file("output/el_markdown_template_files.zip",
    #                  mimetype="application/zip",
    #                  attachment_filename="el_markdown_template_files.zip",
    #                  as_attachment=False)
    response = send_from_directory("./output", 'el_markdown_template_files.zip',
                                   as_attachment=True)
    response.headers["Content-Type"] = "application/zip"
    return response

# TODO: Wrong zip file is offered for download -> find fix

# TODO: Find a way to delete the *.zip file after download


def create_script_files(markdown_file, template_file):
    bash_script = open("files/make_html" + ".bat", "w")
    shell_script = open("files/make_html" + ".sh", "w")
    script_files = [bash_script, shell_script]

    for file in script_files:
        file.write(
            "pandoc -f markdown --template=" + template_file
            + " --css E+L_style.css " + "\"" + markdown_file + "\"" + " -o "
            + "\"" + markdown_file.rstrip(".markdown") + ".html" + "\"")

    bash_script.close()
    shell_script.close()

    return [bash_script.name, shell_script.name]


def create_zip_template_files(archive_file, files) -> 'zip_file':
    myfile = zipfile.ZipFile(archive_file, "w")
    for file in files:
        myfile.write(file, basename(file))
        print(file)
    myfile.close()


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


app.run(debug=True)
