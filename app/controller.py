from flask import Flask, url_for, render_template
import requests
from forms import MovieForm
import psycopg2
from app import app

conn = psycopg2.connect("dbname=grizzledata user=spowell")
cur = conn.cursor()

@app.route('/', methods=["GET", "POST"])
def index(): 
    form = MovieForm()

    do_garbage = []
    if form.validate_on_submit():
        r = requests.get("http://www.omdbapi.com/?s=%s" % form.search.data)
        if r.status_code == 200:
            return render_template("index.html", title="Home", form=form, movies=r.json()) 

    return render_template('index.html', title="Home", form=form, garbage=do_garbage)
