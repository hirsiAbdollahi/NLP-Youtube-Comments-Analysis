from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt


def sentiment_analysis(df):

    # importing and initialising the VADER analyser
    analyzer = SentimentIntensityAnalyzer()

    #Storing the scores in list of dictionaries
    scores = []


    positive, negative, neutral = 0, 0, 0

    for i in range(df['text'].shape[0]):
        compound = analyzer.polarity_scores(df['text'][i])["compound"]

        if compound> 0:
            positive += 1
        elif compound == 0:
            neutral += 1
        elif compound < 0:
            negative += 1


        scores.append({"Compound": compound
    #                        "Positive": pos,
    #                        "Negative": neg,
    #                        "Neutral": neu
                      })
   

    sentiments_score = pd.DataFrame.from_dict(scores)
    df = df.join(sentiments_score)
    
    comments_sentiment_count = {"positive":positive, "negative":negative, "neutral":neutral } 
    return df,  comments_sentiment_count


    
def plot_sentiments (df,comments_sentiment_count, name):

    labels = 'Positive', 'Negative', 'Neutral', 
    sizes = [comments_sentiment_count['positive'], comments_sentiment_count['negative'], comments_sentiment_count['neutral']]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  
    plt.title('Proportion of unique comments with positive, neutral and negative sentiments')
    
    plt.savefig("./flask_app/static/images/plot_sentiments/{}.png".format(name))



def get_most_pos_neg (df):
    pos_idx = df[df.Compound== df.Compound.max()].index[0]
    neg_idx = df[df.Compound== df.Compound.min()].index[0]
    
    most_neg= df.iloc[neg_idx][['text']][0]
    most_pos= df.iloc[pos_idx][['text']][0]
    
    return most_neg,most_pos
    