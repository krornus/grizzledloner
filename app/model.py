from uuid import uuid4
import imghdr
import base64
import requests
from psycopg2 import connect, extras
from hashlib import md5

con = connect(database="grizzledata", user="postgres", host="/tmp", port="5433")
cur = con.cursor(cursor_factory = extras.DictCursor)

def create_queue(name, uname):
    queue_id = str(uuid4())

    cur.execute("SELECT * FROM queues WHERE name = %s", [name])
    
    if cur.fetchone():
        return

    cur.execute("INSERT INTO queues (id, name, uname) VALUES (%s, %s, %s)", (queue_id, name, uname))
    con.commit()

def get_movies(queueid):
    cur.execute("SELECT imdbid FROM queue WHERE id = %s", [queueid])
    imdbids = cur.fetchall()
    if not imdbids:
        return []

    imdbids = tuple([ x[0] for x in imdbids ])
    cur.execute("SELECT * FROM movie WHERE imdbid in %s", (imdbids,))
    return cur.fetchall()

def get_movie(movie_id):
    cur.execute("SELECT * FROM movie WHERE imdbid = %s", (movie_id,))
    result = cur.fetchone()

    if result:
        return result 

    add_movie(movie_id)

    cur.execute("SELECT * FROM movie WHERE imdbid = %s", (movie_id,))
    result = cur.fetchone()

    return result

def get_poster(imdbid):
    cur.execute("SELECT data,mime FROM poster WHERE imdbid = %s", [imdbid])
    return cur.fetchone()[0]

def get_queues(user):
    cur.execute("SELECT name, id FROM queues WHERE uname = %s", [user])

    return cur.fetchall()


def get_queue(name):
    cur.execute("SELECT name, id FROM queues WHERE name = %s", [name])
    return cur.fetchone()

def add_movie(imdbid, queueid=None):

    cur.execute("SELECT title FROM movie WHERE imdbID=%s", [imdbid])
    res = cur.fetchone()

    if queueid:
        enqueue_movie(queueid, imdbid)

    if res:
        return

    url = "http://www.omdbapi.com/?i={}&plot=full&r=json".format(imdbid)
    res = requests.get(url)

    json_data = res.json()
     
    if not json_data:
        return 
                
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

    cur.execute(query.format(",".join(columns), formats),  tuple([json_data[x] for x in columns]))
    con.commit()

    set_poster(json_data['Poster'], imdbid)

def enqueue_move(queueid, imdbid):
    
    cur.execute("SELECT imdbid FROM queue WHERE imdbid = %s AND id = %s", (imdbid, queueid))  
    if cur.fetchone():
        return 

    cur.execute("INSTER  INTO queue (id, imdbid) VALUES(%s, %s)", (queueid, imdbid))
    con.commit()

def set_poster(url, imdbid):
    if url and imdbid:
        r = requests.get(url)
        image = r.content
        mime = imghdr.what("", image)
    
        cur.execute("INSERT INTO poster (data, mime, imdbid) VALUES (%s, %s, %s)", 
            (base64.b64encode(image), 
            mime, 
            imdbid))

        con.commit()

