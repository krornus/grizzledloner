from uuid import uuid4
from psycopg2 import connect
from hashlib import md5

con = connect("dbname=grizzledata user=spowell")
cur = con.cursor()

def user_queues(userid):
    query = "SELECT DISTINCT queueid from queue WHERE userid = %s"
    cur.execute(query, [userid])
    return cur.fetchall()

def add_movie(movieid, userid, queueid, name)
    query = "INSERT INTO queue (movieid, userid, queueid, name) VALUES (%s, %s, %s, %s)"
    cur.execute(query, (movieid, userid, queueid, name))
    con.commit()

def get_queue(queueid):
    query = 'SELECT * FROM queue WHERE queueid=%s'
    cur.execute(query, [queueid])
    return cur.fetchall()

def validate_passwd(username, passwd):
    query = "SELECT passwd FROM account WHERE userid = %s"
    cur.execute(query, [username])
    res = cur.fetchone()
    check = md5(passwd+username).hexdigest()

    if not res:
        return False

    return res[0] == check 

def add_user(username, passwd):
    
    query = "SELECT userid FROM account WHERE userid = %s"
    cur.execute(query, [username])

    if cur.fetchone():
        return False
    
    query = "INSERT INTO account VALUES (%s, %s)"
    digest = md5(passwd+username).hexdigest()

    cur.execute(query, [username, digest])
    con.commit()

    return True
