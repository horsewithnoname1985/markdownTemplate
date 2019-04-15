from mdtemplate.create_form import app, main

url, port = main(autostart=True, debug=False, test=False)
app.run(port=port)
