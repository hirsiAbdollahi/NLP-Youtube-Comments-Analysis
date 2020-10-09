import os
import redis 
import re

from flask import Flask, render_template, url_for, request, redirect, flash

UPLOAD_FOLDER = 'static/images/'

app = Flask(__name__)
app.config.update(SECRET_KEY='flask')
cache = redis.Redis(host='redis', port=6379)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
  return render_template('index.html')


import flask_app.youtube_comments