import os
from flask import Flask, render_template, request
from dat import insertBLOB
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import sys
from PIL import Image
import base64
import six
import io
import PIL.Image
from base64 import b64encode
import mysql.connector
__author__ = 'pierre amir'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

NAME = "pierre"
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return render_template("complete.html")
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                insertBLOB(NAME,file)
    return render_template("complete.html")

@app.route("/index", methods=['POST'])
def display_image():
    db = mysql.connector.connect(host='localhost',
                                             database='school',
                                             user='root',
                                             password='mysql')
    cursor=db.cursor()
    sql1='select data from students where Fname = %s'
    cursor.execute(sql1,(NAME,))
    #db.commit()
    data=cursor.fetchall()
    #print type(data[0][0])
    image = b64encode(data).decode("utf-8")
    db.close()
    return render_template("index.html",data=image)

if __name__ == "__main__":
    app.run()

