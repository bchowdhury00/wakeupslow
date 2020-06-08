from flask import Flask, request, redirect, session, render_template, url_for, flash
import os

app = Flask(__name__)

app.secret_key = os.urandom(32)

@app.route("/")
def hello_world():
    return "!"
@app.route("/another")
def another():
    return

if __name__ == "__main__":
    app.debug = True
    app.run()