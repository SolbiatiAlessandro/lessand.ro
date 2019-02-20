import os
import psycopg2
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
db = conn.cursor()

# this is the syntax to insert
db.execute("INSERT INTO users (username, password) VALUES ({}, {})".format("'test'","'test'"))
conn.commit()

# this is the syntax to select
db.execute("SELECT id FROM users WHERE username = '{}';".format(username))}
print db.fetchone()

db.close()
conn.close()
