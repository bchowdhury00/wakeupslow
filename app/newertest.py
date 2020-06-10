from flask import Flask,render_template
import os
from flask_socketio import SocketIO 
app = Flask(__name__)
app.secret_key = os.urandom(32)
socketio = SocketIO(app)

@app.route('/')
def hello_world():
    return render_template('messages.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)


if __name__ == "__main__":
    app.debug = True
    socketio.run(app)
