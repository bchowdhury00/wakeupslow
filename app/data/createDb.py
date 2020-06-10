import sqlite3

DB_FILE = "data/database.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users(id integer, username text, password text);')
c.execute('CREATE TABLE IF NOT EXISTS listings(id integer, userID integer, itemName text, '
          'itemDescription text, price decimal, picture text, purchasedBy integer);')

db.commit()
