import sqlite3

DB_FILE = "app/data/database.db"

def getNextID(type):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if type == "user":
        arr = c.execute("SELECT MAX (id) FROM users;").fetchall()
    else:
        arr = c.execute("SELECT MAX(id) FROM listings WHERE userID='{}';".format(type)).fetchall()
    print(arr)
    if arr[0][0] == None:
        return 0
    return int(arr[0][0]) + 1

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
        return 0
    elif password != password1:
        return 1
    c.execute('INSERT INTO users(id, username, password) '
              'VALUES({},\"{}\",\"{}\");'.format(getNextID("user"), user, password))
    db.commit()
    return "success"

def getUserInfo(user):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    arr = c.execute('SELECT * FROM users WHERE username=\"{}\"'.format(user)).fetchall()
    print(arr)
    return arr[0]

    
def addListing(user,title,category,description,price,picture):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    arr = c.execute('SELECT id FROM users WHERE username=\"{}\"'.format(user)).fetchall()
    print(arr)
    userID = int(arr[0][0])
    querry = 'INSERT INTO listings(id, userID, itemName, itemCategory, itemDescription, price, picture, purchasedBy) ' \
             'VALUES({},{},\"{}\",\"{}\",\"{}\",{},\"{}\",{});'.format(getNextID(userID), userID, title, category,
                                                                     description, price, picture, 0)
    print(querry)
    c.execute(querry)
    db.commit()
    return "success"

def getFileName(user):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    userID = getUserInfo(user)[0]
    filename = "U{}L{}".format(userID, getNextID(userID))
    print(filename)
    return filename

def updateInfo(user,category,info):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    query = 'UPDATE users SET {} = \"{}\" WHERE id={};'.format(category, info, getUserInfo(user)[0])
    print(query)
    c.execute(query)
    db.commit()
    return True

