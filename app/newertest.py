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
    return render_template('testMesage.html')

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
