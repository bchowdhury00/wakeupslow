import sqlite3

DB_FILE = "app/data/database.db"

def getNextID(type):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if type == "user":
        arr = c.execute("SELECT id FROM users;").fetchall()
    else:
        arr = c.execute("SELECT id FROM listings WHERE userID='{}';".format(type)).fetchall()
    return len(arr)

def authUser(user,password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    arr = c.execute('SELECT * FROM users WHERE username=\"{}\";'.format(user)).fetchall()
    if len(arr) == 0:
        return False
    elif arr[0][2] != password:
        return False
    return True

def newAccount(user,password,password1):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    arr = c.execute('SELECT * FROM users WHERE username=\"{}\"'.format(user)).fetchall()
    if len(arr) > 0:
        return "Username already in use"
    elif password != password1:
        return "Passwords do not match!"
    c.execute('INSERT INTO users(id, username, password, location) '
              'VALUES({},\"{}\",\"{}\",\"null\");'.format(getNextID("user"), user, password))
    db.commit()
    return "success"

    
def addListing(user,title,category,description,price):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    arr = c.execute('SELECT id FROM users WHERE username=\"{}\"'.format(user)).fetchall()
    print(arr)
    userID = int(arr[0][0])
    querry = 'INSERT INTO listings(id, userID, itemName, itemCategory, itemDescription, price, picture, purchasedBy) ' \
             'VALUES({},{},\"{}\",\"{}\",\"{}\",{},\"{}\",{});'.format(getNextID(userID), userID, title, category,
                                                                     description, price, "FILENAME", 0)
    print(querry)
    c.execute(querry)
    db.commit()
    return "success"
