import os
import redis 
import re

from flask import Flask, render_template, url_for, request, redirect, flash


app = Flask(__name__)
app.config.update(SECRET_KEY='flask')
cache = redis.Redis(host='redis', port=6379)

@app.route("/")
def index():
  return render_template('index.html')


@app.route('/results', methods=["POST"])
def results():
    url = request.form.get('url')

    # try:
    # TODO regex pour check url 
        # response = requests.get(url)

        # embedded video
    regex = r"(?:https:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(.+)"
    embedded = re.sub(regex, r"https://www.youtube.com/embed/\1",url)


    # except:
    #     # error message: invalid youtube url video

    #     flash('Invalid url. Please resubmit.')
    #     return redirect(url_for('index'))


  

    return render_template('results.html', page_results=embedded)

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')