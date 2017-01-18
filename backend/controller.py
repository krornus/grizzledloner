from backend import app
from flask import render_template

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/side")
def side():
    return render_template("side.html")