from flask import Flask, request, redirect, session, render_template, url_for, flash
import os
import sqlite3

app = Flask(__name__)
app.secret_key = os.urandom(32)

DB_FILE = "app/data/database.db"


@app.route('/')
def hello_world():
    return render_template('base.html')

@app.route('/another')
def another():
    return render_template('maptest.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/checkLogin')
def checkLogin():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    print(request.args)
    eUser = request.args['username']
    ePass = request.args['password']

    arr = c.execute("SELECT * FROM users WHERE username='{}';".format(eUser)).fetchall()
    print(arr)
    if len(arr) == 0:
        return render_template('login.html', alert="Username or Password incorrect")
    elif arr[0][2] != ePass:
        return render_template('login.html', alert="Username or Password incorrect")

    session['username'] = eUser
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
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    print(request.args)
    arr = c.execute("SELECT * FROM users WHERE username='{}'".format(request.args['username'])).fetchall()
    if len(arr) > 0:
        message = "Username already in use"
        return render_template('register.html', alert=message)
    elif request.args['password'] != request.args['password-repeat']:
        message = "Passwords do not match, please try again"
        return render_template('register.html', alert=message)

    c.execute("INSERT INTO users(id, username, password) "
              "VALUES('{}','{}','{}');".format(getNextID(), request.args['username'], request.args['password']))
    db.commit()
    return render_template('login.html', success="Account Created")

def getNextID():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    arr = c.execute("SELECT id FROM users;").fetchall()
    return len(arr)

if __name__ == "__main__":
    app.debug = True
    app.run()