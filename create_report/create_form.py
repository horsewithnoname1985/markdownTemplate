from flask import Flask, render_template, request

if __name__ == '__main__':


# TODO: Call HTML template

def create_templates(html_content):
    destination = request.form['destination']
    language = request.form['language']
    author = request.form['author']
    date = request.form['date']
    title = request.form['title']
    project = request.form['project']
    version = "1.0"

    if language == 'DE':
        el_template = 'templates/el_template_de.html'
        md_template = 'templates/Test_protocol_template_de.markdown'

    elif language == "EN":
        el_template = 'templates/el_template_en'
        md_template = 'templates/Test_protocol_template_en.markdown'

    create_html_template()

    # Fragen:
    # - Was muss zuerst passieren: Datei kopieren, dann laden, verändern und speichern oder zunächst laden, ändern und
    # an neuem Ort speichern?
    # - Wie speichert man einen geöffneten Inhalt einer Datei als neue Datei ab?
    # Wie sollte der Inhalt verändert werden: über reguläre Asdrücke suchen und tauschen? Sollten im Template bestimmte
    # Platzhaltervariablen verwendet werden, und dann über platzhalter.replace(meine_variable)? Wie werden Strings
    # überhaupt verändert?
    # - Gibt es bereits eine Lösung um per Python ein Markdown Template zu erstellen? (so wie mit Jinja2 für HTML)




'''
  1. Call HTML form -> main method
  2. HTML form is submitted
  3. Script is creating the files:
    * Copy E+L_style.css to specified directory
    * Copy el_template to specified directory
    * Copy markdown template to specified directory
    * Adjust the text of markdown template as specified in HTML (if not specified remove from template)
'''
