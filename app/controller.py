import requests
import psycopg2
from flask import url_for, render_template, redirect, session, request
from forms import *
from app import app
from model import *
from view import *

uname = "krornus"

@app.route('/index', methods=["GET", "POST"])
@app.route('/', methods=["GET", "POST"])
def index(): 
    
    session['queues'] = get_queues(uname) 

    if 'queue' not in session:
        session['queue'] = session['queues'][0]
    
    if 'queue' in request.args:
        session['queue'] = get_queue(request.args.get("queue")) 

    view = View()
    view.queues = session['queues']
    view.queue = session['queue']

    movies = get_movies(session['queue'][1])
    posters = [(x['poster'], x['imdbid']) for x in movies]
    view.posters = cleanse_posters(posters)

    view.form = {"search":MovieForm(), "queue":QueueForm()}

    return render_template('index.html', title="Home", view=view)


@app.route('/add', methods=["GET", "POST"])
def add():
	imdbid = request.args.get("id")
	if not imdbid:
		return redirect(url_for("index"))

	add_movie(imdbid, session['queue'][1])

	return redirect(url_for("index"))


@app.route('/search', methods=["POST"])
def search():

    view = View()
    view.query = request.form['search']
    view.queues = session['queues']
    view.queue = session['queue']
    view.form = {"search":MovieForm(), "queue":QueueForm()}

    url = "http://www.omdbapi.com/?s={}&r=json&page={}".format(view.query, 1)

    res = requests.get(url)

    json_data = res.json() or {"Search":[]}
    view.posters = [(x['Poster'], x['imdbID']) for x in json_data["Search"]]

    return render_template("search.html", 
            title="Search Results - {}".format(view.query), 
            view=view)


@app.route("/movie", methods=["GET", "POST"])
def movie():
    form = PosterForm()
    view = View()
    movie_id = request.args.get("id") or None

    if not movie_id:
        return redirect(url_for("index"))

    movie = get_movie(movie_id)
    poster = get_poster(movie_id)
    movie['actors'] = movie['actors'].decode("utf-8")
    movie['title'] = movie['title'].decode("utf-8")
    movie['plot'] = movie['plot'].decode("utf-8")
    movie['director'] = movie['director'].decode("utf-8")

    view.movie = movie
    view.form['poster'] = PosterForm() 
    view.form['queue'] = QueueForm() 
    view.poster = poster 
    view.queues = session['queues']
    view.queue = session['queue'] 

    return render_template("movie.html", view=view)



@app.route("/update_poster", methods=["POST"])
def update_poster():

    form = PosterForm(request.form)
    set_poster(form.url.data, form.imdbid.data)

    return redirect(url_for("movie", id=form.imdbid.data))
    
def cleanse_posters(posters):
    result = []
    for x in posters:
        if not x[0] or x[0] == "N/A":
            result.append([url_for("static", filename="no_poster.png"), x[1]])
        else:
            result.append([x[0], x[1]])
    return result 

@app.route("/new_queue", methods=["POST"])
def new_queue():
    form = QueueForm(request.form)

    if not form.name.data:
        return redirect(url_for("index"))

    create_queue(form.name.data, uname)
    session['queues'] = get_queues(uname)
    session['queue'] = session['queues'][0]

    return redirect(url_for("index"))
