import sqlite3

DB_FILE = "data/database.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users(id integer, username text, password text);')

db.commit()