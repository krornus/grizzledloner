from uuid import uuid4
from psycopg2 import connect, extras
from hashlib import md5

con = connect(database="grizzledata", user="postgres", host="/tmp", port="5433")
cur = con.cursor(cursor_factory = extras.DictCursor)

def get_movies():
    cur.execute("SELECT * from movie ORDER BY title")
    return cur.fetchall()

def get_movie(movie_id):
    cur.execute("SELECT * from movie WHERE imdbid = %s", (movie_id,))
    return cur.fetchone()

def add_movie(json_data):

    print "adding " + json_data["Title"]
    query = "INSERT INTO movie ({}) VALUES({})"
    columns = [
        "Actors", 
        "Awards", 
        "Country", 
        "Director", 
        "Genre", 
        "Language", 
        "Metascore", 
        "Plot", 
        "Poster", 
        "Rated", 
        "Released", 
        "Response", 
        "Runtime", 
        "Title", 
        "Type", 
        "Writer", 
        "Year", 
        "imdbID", 
        "imdbRating", 
        "imdbVotes"
    ]

    formats = ("%s, " * len(columns))[:-2]
    cur.execute("SELECT title from movie WHERE imdbID=%s", (json_data['imdbID'],))
    res = cur.fetchone()
    if res:
        return
    cur.execute(query.format(",".join(columns), formats),  tuple([json_data[x] for x in columns]))
    con.commit()


def set_poster(url, imdbid):
    if url and imdbid:
        cur.execute("UPDATE movie SET poster=%s WHERE imdbid=%s", (url, imdbid))
        con.commit()

