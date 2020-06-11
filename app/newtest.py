import os
import platform
from flask import Flask, request, redirect, session, render_template, url_for, flash

filExtension = ""

if (platform.system() == "Windows"):
    filExtension = "\\app\\static\\images"
elif (platform.system() == "Darwin" or platform.system() == "Linux"):
        filExtension = "/static/images"


UPLOAD_FOLDER = os.getcwd() + filExtension

app = Flask(__name__)
app.config['IMAGE_UPLOADS'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    print(os.getcwd())
    return render_template("create.html")


@app.route("/addListing", methods=['GET', 'POST'])
def addListing():
        if request.method == "POST":
            if request.files:
                image = request.files["image"]
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
                print(image)
                return redirect(request.url)

        return ""

if __name__ == '__main__':
    app.run()
