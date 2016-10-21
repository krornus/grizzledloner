import requests
import psycopg2
from flask import url_for, render_template, redirect, session, request
from forms import *
from app import app
from model import *

@app.route('/index', methods=["GET", "POST"])
@app.route('/', methods=["GET", "POST"])
def index(): 

	movies = get_movies()
	posters = [(x['poster'], x['imdbid']) for x in movies]

	form = MovieForm(request.form)
	return render_template('index.html', title="Home", posters=cleanse_posters(posters), search_form=form)


@app.route('/add', methods=["GET", "POST"])
def add():
	movie_id = request.args.get("id")
	if not movie_id:
		return redirect(url_for("index"))

	url = "http://www.omdbapi.com/?i={}&plot=full&r=json".format(movie_id)
	res = requests.get(url)
	
	json_data = res.json()
	
	if not json_data:
		return redirect(url_for("index"))

	add_movie(json_data)


	return redirect(url_for("index"))

@app.route('/search', methods=["POST"])
def search():
	form = MovieForm(request.form)
	query = form.search.data

	url = "http://www.omdbapi.com/?s={}&r=json&page={}".format(query, 1)
	
	res = requests.get(url)
	posters = []


	json_data = res.json() or {"Search":[]}
	posters = [(x['Poster'], x['imdbID']) for x in json_data["Search"]]

	
	
	return render_template("search.html", 
			query=query,
			title="Search Results - {}".format(query), 
			search_form=form, 
			posters=posters)


@app.route("/movie", methods=["GET", "POST"])
def movie():
	form = PosterForm()
	movie_id = request.args.get("id") or None

	if not movie_id:
		return redirect(url_for("index"))

	movie = get_movie(movie_id)
	movie['actors'] = movie['actors'].decode("utf-8")
	movie['title'] = movie['title'].decode("utf-8")
	movie['plot'] = movie['plot'].decode("utf-8")
	movie['director'] = movie['director'].decode("utf-8")

	return render_template("movie.html", movie=movie, form=form)



@app.route("/update_poster", methods=["POST"])
def update_poster():

    form = PosterForm(request.form)
    set_poster(form.url.data, form.imdbid.data)

    return redirect(url_for("movie", id=form.imdbid.data))
    
def cleanse_posters(posters):
    result = []
    for x in posters:
        if x[0] == "N/A":
            result.append([url_for("static", filename="no_poster.png"), x[1]])
        else:
            result.append([x[0], x[1]])
    return result 

