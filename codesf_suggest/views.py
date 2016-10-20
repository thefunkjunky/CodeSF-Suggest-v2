from flask import render_template

from codesf_suggest.main import app

@app.route("/")
def index():
    return app.send_static_file("index.html")
