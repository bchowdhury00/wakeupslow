from flask import Flask, request, redirect, session, render_template, url_for, flash
import os
from data.dbfunc import *
app = Flask(__name__)
app.secret_key = os.urandom(32)

DB_FILE = "data/database.db"


@app.route('/')
def hello_world():
    if 'username' in session:
        return redirect(url_for('home'))
    return render_template('landing.html')

@app.route('/home')
def home():
    if len(request.args)>0:
        if request.args['mType']=='0':
            return render_template('home.html', alert="Username or Password incorrect")
        elif request.args['mType']=='1':
            return render_template('home.html', success="Logged In")
        else:
            return render_template('home.html', success="Listing Added")
    return render_template('home.html')

@app.route('/another')
def another():
    return render_template('maptest.html')

@app.route('/login')
def login():
    if len(request.args) > 0:
        if request.args['mType']=='0':
            return render_template('login.html', alert="Username or Password incorrect")
        else:
            return render_template('login.html', success="Account Created")
    return render_template('login.html')

@app.route('/checkLogin')
def checkLogin():
    eUser = request.args['username']
    ePass = request.args['password']
    if (not authUser(eUser,ePass)):
        return redirect(url_for('login', mType=0))
    session['username'] = eUser
    return redirect(url_for('home', mType=1))

@app.route('/logOut')
def logOut():
    session.pop('username')
    return render_template('base.html', success="Logged Out")

@app.route('/register')
def register():
    if len(request.args)>0:
        if request.args['mType']=='0':
            return render_template('register.html', alert="Username in use")
        else:
            return render_template('register.html', alert="Passwords do not match")
    return render_template('register.html')

@app.route('/createAccount')
def createAccount():
    print(request.args)
    user = request.args['username']
    pass0 = request.args['password']
    pass1 = request.args['password-repeat']
    message = newAccount(user, pass0, pass1)
    if (message != "success"):
        return redirect(url_for('register', mType=message))
    return render_template('base.html', success="Logged Out")

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
    return redirect(url_for('home', mType=2))


if __name__ == "__main__":
    app.debug = True
    app.run()
