import os
import psycopg2
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
db = conn.cursor()                                              db.execute("INSERT INTO users (username, password) VALUES ({}, {})".format("'test'","'test'"))
conn.commit()
db.close()
conn.close()
