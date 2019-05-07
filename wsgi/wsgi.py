from mdtemplate.mdtemplate import app, main

url, port = main(autostart=True)
app.run(port=port)

