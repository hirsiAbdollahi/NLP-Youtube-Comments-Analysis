from flask_app  import app
from flask import Flask, render_template, url_for, request, redirect, flash
import re
from PIL import Image
import os 
import json
import time

from database.db import Database
from scrap.get_comments import main
from models.preprocessing import Preprocess
from models.wordcloud import get_wordcloud
from models.ner import ner_spacey
from models.utils import plot_10_most_common_words
from models.vader_sentiments import *



def insert_todb (table_name,data):
    db = Database()
    db.add_table(table_name)
    db.insert(table_name,data)
    db.close_connection()


def clean_data(df):
    prepro =Preprocess()
    liste= []
    for i in df['text']:
      liste.append(prepro.preprocess(i))
    
    return liste


def display_wordcloud (liste,name):

    if os.path.isfile("./flask_app/static/images/wordcloud/{}.png".format(name)) is False:
        get_wordcloud(liste, str(name))

    filename = "images/wordcloud/{}.png".format(name)

    return filename

def display_topwords (corpus,name):
    
    if os.path.isfile("./flask_app/static/images/{}.png".format(name)) is False:
        plot_10_most_common_words(corpus, str(name))

    filename = "images/{}.png".format(name)

    return filename


def display_sentiments (df,name):
    
    df_sentiments, comments_sentiment_count = sentiment_analysis(df)

    if os.path.isfile("./flask_app/static/images/plot_sentiments/{}.png".format(name)) is False:
        
        plot_sentiments (df, comments_sentiment_count,str(name))

    filename = "images/plot_sentiments/{}.png".format(name)

    most_neg,most_pos= get_most_pos_neg(df_sentiments)


    return filename, most_neg,most_pos

@app.route('/results', methods=["POST"])
def results():
    # Youtube regex 
    regex = r"(?:https:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(.+)"

    # url from the user 
    url = request.form.get('url')

    if re.match(regex, url):

        #scrape comment from the youtube video 
        df = main(url)

        # insert comment into the db
        # insert_todb('salut1', df)
        
        # clean text before using it for wordcloud
        #TODO save it in csv for later use 
        clean_liste_text = clean_data(df) 

        ## wordcloud
        filename_wordcloud = display_wordcloud(clean_liste_text,'coucou')
       
        ## NER
        person_counts,norp_counts,fac_counts,org_counts,gpe_counts,loc_counts,product_counts,event_counts = ner_spacey(df)

        # 10 most commond words 
        filename_common_words= display_topwords(clean_liste_text,'coucou')

        # Sentiments analysis
        filename_sentiment, most_neg,most_pos= display_sentiments(df,'coucou')


    else: 
        flash('Invalid url. Please resubmit.')
        return redirect(url_for('index'))

  

    return render_template('results.html', filename_wordcloud =filename_wordcloud,filename_common_words=filename_common_words,
                          person_counts=person_counts,norp_counts=norp_counts,fac_counts=fac_counts,org_counts=org_counts,gpe_counts=gpe_counts,loc_counts=loc_counts,product_counts=product_counts,event_counts=event_counts,
                         filename_sentiment=filename_sentiment, most_neg=most_neg,most_pos=most_pos,        )




if __name__ == "__main__":
    # app.run()
    app.run(debug=True, host='0.0.0.0')