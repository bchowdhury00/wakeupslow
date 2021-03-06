from flask import Flask, request, redirect, session, render_template, url_for, flash
import os, platform, json
from flask_socketio import SocketIO,join_room, leave_room
from data.dbfunc import *

key = ""
UPLOAD_FOLDER = ""

if (platform.system() == "Windows"):
    UPLOAD_FOLDER = os.getcwd() + "\\app\\static\\images"
elif (platform.system() == "Darwin" or platform.system() == "Linux"):
        UPLOAD_FOLDER = 'static/images/'

app = Flask(__name__)
app.secret_key = os.urandom(32)
# UPLOAD_FOLDER = './static/images/'
app.config['IMAGE_UPLOADS'] = UPLOAD_FOLDER
DB_FILE = "data/database.db"
socketio = SocketIO(app)


def getKey():
    f = open('../key.txt')
    return f.read()

key = getKey()
print(key)

@app.route('/')
def hello_world():
    if 'username' in session:
        return redirect(url_for('home'))
    return render_template('landing.html')


@app.route('/home')
def home():
    if len(request.args) > 0:
        if request.args['mType'] == '0':
            return render_template('home.html', alert="?", key=key)
        elif request.args['mType'] == '1':
            return render_template('home.html', listings=getListings(session['username']), success="Logged In", key=key)
        elif request.args['mType'] == '2':
            return render_template('home.html', listings=getListings(session['username']), success="Listing Added", key=key)
        else:
            return render_template('landing.html', success="Logged Out", key=key)
    if 'username' not in session:
        return redirect('/')
    return render_template('home.html', listings=getListings(session['username']), key = key)

@app.route('/home/<category>')
def li(category):
    listings = getListings('c')
    filtered = {}
    for idx in listings:
        if listings[idx]['type'] == category:
            filtered[len(filtered)] = listings[idx]
    print(category)
    return render_template('home.html', listings=filtered, cat=str(category), key=key)

@app.route('/listings/<listingID>', methods=['GET','POST'])
def viewListing(listingID):
    arr = listingID[1:].split('L')
    listingInfo = getListing(int(arr[0]), int(arr[1]))
    if request.method == 'POST':
        buyerName = request.form['buyerUsername']
        print(buyerName)
        if len(getUserInfo(buyerName)) > 0:
            print(getUserInfo(buyerName)[0])
            listing = markSold(listingID,buyerName)
            return render_template("viewListing.html", listing=listingInfo, success='Marked as Sold')
        else:
            return render_template("viewListing.html", listing=listingInfo, alert='Invalid buyer username')
    return render_template("viewListing.html", listing=listingInfo)


@app.route('/another')
def another():
    return render_template('maptest.html')


#################ACCOUNTS####################
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if len(request.args) > 0:
            if request.args['mType'] == '0':
                return render_template('login.html', alert="Username or Password incorrect")
            elif request.args['mType'] == '1':
                return render_template('login.html', success="Account Created")
            else:
                return render_template('login.html', alert="You must be logged in")
        return render_template('login.html')
    else:
        eUser = request.form['username']
        ePass = request.form['password']
        if not authUser(eUser, ePass):
            return redirect(url_for('login', mType=0))
        session['username'] = eUser
        return redirect(url_for('home', mType=1))


@app.route('/logOut')
def logOut():
    session.pop('username')
    return redirect(url_for('home', mType=3))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        if len(request.args) > 0:
            if request.args['mType'] == '0':
                return render_template('register.html', alert="Username in use")
            else:
                return render_template('register.html', alert="Passwords do not match")
        return render_template('register.html')
    else:
        print(request.form)
        user = request.form['username']
        pass0 = request.form['password']
        pass1 = request.form['password-repeat']
        message = newAccount(user, pass0, pass1)
        if (message != "success"):
            return redirect(url_for('register', mType=message))
        return render_template('base.html', success="Account Created")


#################PROFILES####################
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'GET':
        arr = getUserInfo(session['username'])
        print(arr)
        if len(request.args) > 0:
            if request.args['mType']=='0':
                return render_template('profileInfo.html', userInfo=arr, success='Updated Location', key=key)
            elif request.args['mType']=='1':
                return render_template('profileInfo.html', userInfo=arr, success='Updated Contact Info', key=key)
            elif request.args['mType']=='2':
                return render_template('profileInfo.html', userInfo = arr, alert='You Must Log a Valid Location to Create a Listing', key=key)
            elif request.args['mType']=='3':
                return render_template('profileInfo.html', userInfo = arr, alert='Invalid Location', key=key)
        return render_template('profileInfo.html', userInfo=arr, key=key)
    else:
        if request.get_json():
            newlocation = request.get_json()
            print(newlocation)
            message = 'Updated Location'
            res = {"redirect": "/profile?mType=0", "message":message}
            updateInfo(session['username'], 'location', newlocation)
            return res
        else:
            arr = request.form
            print(arr)
            updateInfo(session['username'], 'contactInfo', request.form['contact'])
            return redirect(url_for('profile', mType=1))


@app.route('/profile/myListings/active')
def myListings():
    data = getMyListings(session['username'], True)
    return render_template('profileListings.html', listings=data, category='myActive')


@app.route('/profile/myListings/sold')
def mySold():
    data = getMyListings(session['username'], False)
    return render_template('profileListings.html', listings=data, category='mySold')


@app.route('/profile/myPurchases')
def myPurchases():
    data = getMyPurchased(session['username'])
    return render_template('profileListings.html', listings=data, category='purchases')


@app.route('/createListing', methods=['GET', 'POST'])
def createListing():
    location = getUserInfo(session['username'])[3]
    if request.method == 'GET':
        return render_template('create.html', location = location, key=key)
    else:
        if 'username' not in session:
            return redirect(url_for('login', mType=2))
        results = request.form
        print(results)
        filename = getFileName(session['username'])
        if results['title'] == "" and results['price'] == "":
            return render_template('create.html', location = location, key=key, alert="You Must Enter a Title And a Price")
        if results['title'] == "":
            return render_template('create.html', location = location, key=key, alert="You Must Enter a Title")
        if results['price'] == "":
            return render_template('create.html', location = location, key=key, alert="You Must Enter a Price")
        if request.files:
            image = request.files["image"]
            ext = image.filename.split('.')[-1]
            print(ext)
            if filename == "":
                filename = "index"
                ext = "png"
            filename += ("." + ext)
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
        print(filename)
        addListing(session['username'], results['title'], results['category'], results['description'], results['price'],
                   filename)
        return redirect(url_for('home', mType=2))


@app.route('/allmessages')
def viewMyMessages():
    if 'username' not in session:
        return redirect(url_for('login', mType=2))
    arr = getOpenConvos(session['username'])
    if arr != []:
        return redirect(url_for("message",otheruser=arr[0]))
    else:
        return redirect(url_for("message",otheruser='None'))


@app.route('/messages/<otheruser>',methods=['GET', 'POST'])
def message(otheruser):
    if 'username' not in session:
        return redirect(url_for('login', mType=2))
    if otheruser == 'None':
        return render_template('messages.html', myusername=session['username'])
    user = session['username']
    user2= getUserInfo(otheruser)[1]
    history = json.dumps(getConvo(user,user2))
    print(history)
    chatroom = json.dumps(getChatRoom(user,otheruser))
    arr = getOpenConvos(session['username'])
    return render_template("messages.html",people=arr,other=user2,room=chatroom,myusername=json.dumps(user),username2=json.dumps(user2),hist=history)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')
    return

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    roomname = json['room']
    user1= getUserInfo(json['user_name'])[0]
    user2= getUserInfo(json['other_user'])[0]
    #print(roomname)
    if (json['message'] == ""):
        return
    addMessage(user1,user2,json['message'],json['time'])
    socketio.emit('my response',json,room=roomname,callback=messageReceived)
    return

@socketio.on('join')
def on_join(data,methods=['GET', 'POST']):
    username = data['username']
    room = data['room']
    join_room(room)
    socketio.send(username + ' has entered the room.', room=room)

@socketio.on('leave')
def on_leave(data,methods=['GET', 'POST']):
    username = data['username']
    room = data['room']
    leave_room(room)
    socketio.send(username + ' has left the room.', room=room)

if __name__ == "__main__":
    app.debug = True
    socketio.run(app)
