
import sys
print(sys.path)
from database.db import Database
from scrap.get_comments import main
from flask_app  import app


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

  

    return render_template('results.html', page_results=df)

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')