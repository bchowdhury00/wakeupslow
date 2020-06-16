import sqlite3
import json
import random
import string


DB_FILE = "data/database.db"

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
    if isinstance(user, str):
        arr = c.execute('SELECT * FROM users WHERE username=\"{}\";'.format(user)).fetchall()
    else:
        arr = c.execute('SELECT * FROM users WHERE id={};'.format(user)).fetchall()
    if len(arr)>0:
        return arr[0]
    return []


def addListing(user,title,category,description,price,picture):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    arr = c.execute('SELECT id FROM users WHERE username=\"{}\"'.format(user)).fetchall()
    print(arr)
    userID = int(arr[0][0])
    querry = 'INSERT INTO listings(id, userID, itemName, itemCategory, itemDescription, price, picture, purchasedBy) ' \
             'VALUES({},{},\"{}\",\"{}\",\"{}\",{},\"{}\",{});'.format(getNextID(userID), userID, title, category,
                                                                     description, price, picture, -1)
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

def getListings(user):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    userID = getUserInfo(user)[0]
    result={}
    selected = c.execute('SELECT * FROM listings WHERE userID != {} AND purchasedBy = -1;'.format(userID)).fetchall()
    for i in range(len(selected)):
        arr = selected[i]
        entry={}
        entry['listingID'] = 'U{}L{}'.format(arr[1],arr[0])
        entry['title'] = arr[2]
        entry['vendor'] = getUserInfo(arr[1])[1]
        entry['imagesrc'] = 'static/images/' + arr[6]
        if (getUserInfo(arr[1])[3] == None):
            entry['location'] = "None"
        else:
            entry['location'] = getUserInfo(arr[1])[3]
        entry['price'] = arr[5]
        entry['type'] = arr[3]
        result[i] = entry
    return result

def getListing(userID, listingID):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    arr=c.execute('SELECT * FROM listings WHERE userID={} AND id={};'.format(userID, listingID)).fetchall()[0]
    entry = {}
    entry['title'] = arr[2]
    entry['vendor'] = getUserInfo(arr[1])[1]
    entry['imagesrc'] = 'static/images/' + arr[6]
    entry['location'] = getUserInfo(arr[1])[4]
    entry['price'] = arr[5]
    entry['type'] = arr[3]
    if arr[7] != -1:
        entry['purchasedBy'] = getUserInfo(arr[7])[1]
    print(entry)
    return entry

def getMyListings(user,active):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    userID = getUserInfo(user)[0]
    result={}
    if active:
        selected = c.execute('SELECT * FROM listings WHERE userID = {} and purchasedBy = -1;'.format(userID)).fetchall()
    else:
        selected = c.execute('SELECT * FROM listings WHERE userID = {} and purchasedBy != -1;'.format(userID)).fetchall()
    for i in range(len(selected)):
        arr = selected[i]
        print(arr)
        entry={}
        entry['listingID'] = 'U{}L{}'.format(arr[1],arr[0])
        entry['title'] = arr[2]
        entry['imagesrc'] = 'static/images/' + arr[6]
        entry['price'] = arr[5]
        entry['type'] = arr[3]
        if not active:
            entry['soldTo'] = getUserInfo(arr[7])[1]
        result[i] = entry
    return result

def getMyPurchased(user):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    userID = getUserInfo(user)[0]
    result = {}
    selected = c.execute('SELECT * FROM listings WHERE purchasedBy = {};'.format(userID)).fetchall()
    for i in range(len(selected)):
        arr = selected[i]
        entry={}
        entry['listingID'] = 'U{}L{}'.format(arr[1],arr[0])
        entry['title'] = arr[2]
        entry['vendor'] = getUserInfo(arr[1])[1]
        entry['imagesrc'] = 'static/images/' + arr[6]
        entry['location'] = getUserInfo(arr[1])[4]
        entry['price'] = arr[5]
        entry['type'] = arr[3]
        result[i] = entry
    return result

#SELECT * FROM messages WHERE (fromUser = 0 AND toUser = 2) OR (fromUser = 2 and toUser = 0);


def getConvo(fromUser, toUser):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    fromID = getUserInfo(fromUser)[0]
    toID = getUserInfo(toUser)[0]
    usernames={}
    usernames[fromID] = fromUser
    usernames[toID] = toUser
    result = {}
    result['fromUser'] = fromUser
    result['toUser'] = toUser
    arr = c.execute('SELECT * FROM messages WHERE (fromUser={} and toUser={}) or (fromUser={} and toUser={});'.format(fromID, toID, toID, fromID)).fetchall()
    print(packageMessages(arr,usernames))
    result['messages'] = packageMessages(arr,usernames)
    json_object = json.dumps(result, indent=4)
    return json_object


def packageMessages(arr,usernames):
    result={}
    for i in range(len(arr)):
        temp={}
        temp['fromUser'] = usernames[arr[i][0]]
        temp['content'] = arr[i][2]
        temp['timestamp'] = arr[i][3]
        result[i] = temp
    return result

def getOpenConvos(user):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    userID = getUserInfo(user)[0]
    result=[]
    arr = c.execute('SELECT toUser FROM messages WHERE fromUser={};'.format(userID)).fetchall()
    #print(arr)
    for elem in arr:
        name = getUserInfo(elem[0])[1]
        if name not in result:
            result.append(name)
    arr = c.execute('SELECT fromUser FROM messages WHERE toUser={};'.format(userID)).fetchall()
    #print(arr)
    for elem in arr:
        name = getUserInfo(elem[0])[1]
        if name not in result:
            result.append(name)
    return result

def addMessage(fromUser,toUser,content,timestamp):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('INSERT INTO messages(fromUser,toUser,content,tStamp) '
              'VALUES(\"{}\",\"{}\",\"{}\",\"{}\");'.format(fromUser,toUser,content,timestamp))
    db.commit()
    return

def createChatRoom(stringLength):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

def getChatRoom(user1,user2):
    id1 = getUserInfo(user1)[0]
    id2 = getUserInfo(user2)[0]
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    arr = c.execute('SELECT roomname FROM chatrooms WHERE (user1={} and user2={}) or (user1={} and user2={});'.format(id1, id2, id2, id1)).fetchall()
    if (len(arr) > 0):
        return arr[0][0]
    rname = createChatRoom(10)
    querry = 'INSERT INTO chatrooms(user1,user2,roomname) VALUES({},\"{}\",\"{}\");'.format(id1, id2, rname)
    c.execute(querry)
    db.commit()
    return rname

def markSold(listingID,buyerName):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    arr = listingID[1:].split('L')
    buyerID = getUserInfo(buyerName)[0]
    c.execute('UPDATE listings SET purchasedBy={} WHERE userID={} AND id={};'.format(buyerID,arr[0],arr[1]))
    db.commit()
    return getListing(int(arr[0]),int(arr[1]))
