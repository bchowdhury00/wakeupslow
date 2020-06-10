from flask import Flask, request, redirect, session, render_template, url_for, flash
import os
from app.data.dbfunc import *
app = Flask(__name__)
app.secret_key = os.urandom(32)

DB_FILE = "data/database.db"


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
    eUser = request.args['username']
    ePass = request.args['password']
    if (not authUser(eUser,ePass)):
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
    print(request.args)
    user = request.args['username']
    pass0 = request.args['password']
    pass1 = request.args['password-repeat']
    message = newAccount(user, pass0, pass1)
    if (message != "success"):
        return render_template('register.html', alert=message)
    return render_template('login.html', success="Account Created")

@app.route('/profile')
def profile():
    arr = getUserInfo(session['username'])
    print(arr)
    return render_template('profile.html', userInfo=arr)


@app.route('/createListing')
def createListing():
    return render_template('create.html')

@app.route('/addListing')
def addL():
    results = request.args
    print(results)
    addListing(session['username'],results['title'],results['category'],results['description'],results['price'])
    return render_template('base.html', success="Listing Added")


if __name__ == "__main__":
    app.debug = True
    app.run()
