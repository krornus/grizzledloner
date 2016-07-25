from flask import Flask, url_for, render_template, redirect, session, request
import requests
from forms import *
import psycopg2
from app import app
from uuid import uuid4
from model import *

@app.route('/', methods=["GET", "POST"])
def index(): 
    form = MovieForm()

    do_garbage = []
    if form.validate_on_submit():
        r = requests.get("http://www.omdbapi.com/?s=%s" % form.search.data)
        if r.status_code == 200:
            json = r.json()
            if json and "Search" in json:
                json = json['Search']
                add_movie(
                    json[0]['imdbID'], 
                    session['username'], 
                    "24827466-fbf4-4263-8339-6306adefa81d",
                    "queue1")

            return redirect(url_for("index"))

    movies = []
    for queue in user_queues(session['username']):
        for row in get_queue(queue[0]):
            r = requests.get("http://www.omdbapi.com/?i=%s" % row[1])
            try:
                movies.append(r.json()['Poster'])
            except:
                pass

    return render_template('index.html', title="Home", form=form, movies=movies)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        
        if validate_passwd(form.username.data, form.password.data):
            session['username'] = form.username.data
            session['logged'] = True
            return redirect(url_for("index"))
        else:
            return redirect(url_for("login", error=True))

    return render_template("login.html", title="Log In", form=form, error=request.args.get("error"))

@app.route('/register', methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if not add_user(form.username.data, form.password.data):
            return redirect(url_for("register", error=True))

        return redirect(url_for("login"))

    return render_template("register.html", 
        title="Register", 
        form=form, 
        error=request.args.get("error"))
