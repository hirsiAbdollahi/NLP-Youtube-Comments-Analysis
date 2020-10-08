import sys
print(sys.path)
from database.db import Database
from scrap.get_comments import main
from flask_app  import app
from flask import Flask, render_template, url_for, request, redirect, flash
import re


@app.route('/results', methods=["POST"])
def results():
    # Youtube regex 
    regex = r"(?:https:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(.+)"

    # url from the user 
    url = request.form.get('url')

    if re.match(regex, url):
        
        #scrape comment 
        df = main(url)

    else: 
        flash('Invalid url. Please resubmit.')
        return redirect(url_for('index'))

  

    return render_template('results.html', tables=[df.to_html(classes='data')], titles=df.columns.values)

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')