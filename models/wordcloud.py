# import numpy as np
# 
from wordcloud import WordCloud
# from models.preprocessing 


def get_wordcloud (liste,name):

    #flat list + joint
    flat_list = [item for sublist in liste for item in sublist] 
    flat_liste_join =' '.join(flat_list)

    #wordcloud
    wc = WordCloud(background_color="black", max_words=100)

    wc.generate(flat_liste_join)
    # plt.figure(figsize = (8, 8)) 
    # plt.axis("off") 
    # plt.tight_layout(pad = 0)
    # plt.imshow(wc) 
    # plt.show()
    wc.to_file("./flask_app/static/images/wordcloud/{}.png".format(name))

