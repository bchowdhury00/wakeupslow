from flask import Flask, request, redirect, session, render_template, url_for, flash
import os
import sqlite3
from data.dbfunc import *
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './static/images/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'img'}

app = Flask(__name__)
app.secret_key = os.urandom(32)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DB_FILE = "data/database.db"


@app.route('/home')
def hello_world():
    listings = {
        "listing1" : {
            "title" : "title1",
            "vendor" : "username",
            "imagesrc" : "static/images/index.png",
            "location" : "Brooklyn NY",
            "price" : "00.00",
            "type" : "Lacrosse"
        }
    }
    return render_template('home.html', listings = listings)


@app.route('/another')
def another():
    return render_template('maptest.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/checkLogin')
def checkLogin():
    eUser = request.args['username']
    ePass = request.args['password']
    if (not authUser(eUser, ePass)):
        return render_template('login.html', alert="Username or Password incorrect")
    session['Username'] = eUser
    return render_template('base.html', success="Logged in")


@app.route('/logOut')
def logOut():
    session.pop('username')
    return render_template('base.html', success='Logged Out')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/createAccount')
def createAccount():
    print(request.args)
    user = request.args['username']
    pass0 = request.args['password']
    pass1 = request.args['password-repeat']
    message = newAccount(user, pass0, pass1)
    if (message != "sucess"):
        return render_template('register.html', alert=message)
    return render_template('login.html', success="Account Created")


@app.route('/createListing')
def createListing():
    return render_template('create.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploadPicture', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('createListing',
                                    filename=filename))
    return ''



if __name__ == "__main__":
    app.debug = True
    app.run()
