import json
from psycopg2 import connect

conn = connect("dbname=grizzledata user=spowell")
cur = conn.cursor()
with open("json", "r") as f:
    data = f.read()
    data = json.loads(data)

query = "CREATE TABLE movie ("
for key in data.keys():
    query += "%s TEXT, " % key.lower()

query += "id serial PRIMARY KEY);"

cur.execute(query)
conn.commit()
