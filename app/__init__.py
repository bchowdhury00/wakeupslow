from flask import Flask, request, redirect, session, render_template, url_for, flash
import os

app = Flask(__name__)

app.secret_key = os.urandom(32)

@app.route('/')
def hello_world():
    return render_template('base.html')
@app.route('/another')
def another():
    return render_template('maptest.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/createAccount')
def createAccount():
    return "createAccount"
if __name__ == "__main__":
    app.debug = True
    app.run()