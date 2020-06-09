import sqlite3

DB_FILE = "data/database.db"

def getNextID():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    arr = c.execute("SELECT id FROM users;").fetchall()
    return len(arr)

def authUser(user,password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    arr = c.execute("SELECT * FROM users WHERE username='{}';".format(user)).fetchall()
    if len(arr) == 0:
        return False
    elif arr[0][2] != password:
        return False
    return True

def newAccount(user,password,password1):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    arr = c.execute("SELECT * FROM users WHERE username='{}'".format(user)).fetchall()
    if len(arr) > 0:
        return "Username already in use"
    elif password != password1:
        return "Passwords do not match!"
    c.execute("INSERT INTO users(id, username, password) "
              "VALUES('{}','{}','{}');".format(getNextID(), user, password))
    db.commit()
    return "success"

    

