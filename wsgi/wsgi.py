from mdtemplate.create_form import app, main

url, port = main(autostart=True, debug=False)
app.run(port=port)
