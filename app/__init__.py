from flask import Flask, request, redirect, session, render_template, url_for, flash
import os
from app.data.dbfunc import *

app = Flask(__name__)
app.secret_key = os.urandom(32)
UPLOAD_FOLDER = os.getcwd() + "/app/static/images"
app.config['IMAGE_UPLOADS'] = UPLOAD_FOLDER
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
        elif request.args['mType']=='2':
            return render_template('home.html', success="Listing Added")
        else:
            return render_template('landing.html', success= "Logged Out")
    return render_template('home.html')

@app.route('/another')
def another():
    return render_template('maptest.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if len(request.args) > 0:
            if request.args['mType']=='0':
                return render_template('login.html', alert="Username or Password incorrect")
            else:
                return render_template('login.html', success="Account Created")
        return render_template('login.html')
    else:
        eUser = request.form['username']
        ePass = request.form['password']
        if (not authUser(eUser, ePass)):
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
        if len(request.args)>0:
            if request.args['mType']=='0':
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



@app.route('/profile')
def profile():
    arr = getUserInfo(session['username'])
    print(arr)
    return render_template('profile.html', userInfo=arr)


@app.route('/createListing', methods=['GET', 'POST'])
def createListing():
    if request.method == 'GET':
        return render_template('create.html')
    else:
        results = request.form
        print(results)
        filename = ""
        if request.files:
            image = request.files["image"]
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            filename = image.filename
            print('')
            print(image)
        addListing(session['username'], results['title'], results['category'], results['description'], results['price'],
                   filename)
        return redirect(url_for('home', mType=2))



if __name__ == "__main__":
    app.debug = True
    app.run()
