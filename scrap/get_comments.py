import requests
import json
import time
import pandas as pd

from datetime import datetime
from dateutil.relativedelta import relativedelta
import re

def date_datetime(x):
    ''' Youtube comment date always say "il y'a 1 mois" or "il y'a 3 ans" 
        this function transform it to datetime object"
    '''
    #  remove "il ya" part
    x= x.replace('il y a ','')

    # regex to distinguish "an/ans", "mois" and "heure"
    if re.search('an',x):
        x =int(re.findall(r'[0-9]+', x)[0])
        time = datetime.now() - relativedelta(years=x)
        
    if re.search('moi',x):
        x =int(re.findall(r'[0-9]+', x)[0])
        time = datetime.now() - relativedelta(months=x)
        
    else:
        x =int(re.findall(r'[0-9]+', x)[0])
        time = datetime.now() - relativedelta(hours=x)
    
    return time

# from https://github.com/egbertbouman/youtube-comment-downloader
def search_dict(partial, key):
    """
    A handy function that searches for a specific `key` in a `partial` dictionary/list
    """
    if isinstance(partial, dict):
        for k, v in partial.items():
            if k == key:
                # found the key, return the value
                yield v
            else:
                # value of the dict may be another dict, so we search there again
                for o in search_dict(v, key):
                    yield o
    elif isinstance(partial, list):
        # if the passed data is a list
        # iterate over it & search for the key at the items in the list
        for i in partial:
            for o in search_dict(i, key):
                yield o

# from https://github.com/egbertbouman/youtube-comment-downloader
def find_value(html, key, num_sep_chars=2, separator='"'):
    # define the start position by the position of the key + 
    # length of key + separator length (usually : and ")
    start_pos = html.find(key) + len(key) + num_sep_chars
    # the end position is the position of the separator (such as ")
    # starting from the start_pos
    end_pos = html.find(separator, start_pos)
    # return the cAontent in this range
    return html[start_pos:end_pos]



def main(url):
    session = requests.Session()
    # make the request
    res = session.get(url)

    
    # extract the XSRF token
    xsrf_token = find_value(res.text, "XSRF_TOKEN", num_sep_chars=3)


    # parse the YouTube initial data in the <script> tag
    data_str = find_value(res.text, 'window["ytInitialData"] = ', num_sep_chars=0, separator="\n").rstrip(";")
    # convert to Python dictionary instead of plain text string
    data = json.loads(data_str)


    # search for the ctoken & continuation parameter fields
    for r in search_dict(data, "itemSectionRenderer"):
        pagination_data = next(search_dict(r, "nextContinuationData"))
        if pagination_data:
            # if we got something, break out of the loop,
            # we have the data we need
            break
    continuation_tokens = [(pagination_data['continuation'], pagination_data['clickTrackingParams'])]


    df = pd.DataFrame(columns=["commentId", "text", "time", "likeCount", 'author', 'channel',"authorIsChannelOwner"])
    while continuation_tokens:
        # keep looping until continuation tokens list is empty (no more comments)
        continuation, itct = continuation_tokens.pop()
        # construct params parameter (the ones in the URL)
        params = {
            "action_get_comments": 1,
            "pbj": 1,
            "ctoken": continuation,
            "continuation": continuation,
            "itct": itct,
        }
        # construct POST body data, which consists of the XSRF token
        data = {
            "session_token": xsrf_token,
        }
        # construct request headers
        headers = {
            "x-youtube-client-name": "1",
            "x-youtube-client-version": "2.20200731.02.01"
        }
        # make the POST request to get the comments data
        response = session.post("https://www.youtube.com/comment_service_ajax", params=params, data=data, headers=headers)
        # convert to a Python dictionary
        comments_data = json.loads(response.text)
       
        for comment in search_dict(comments_data, "commentRenderer"):
            df = df.append(
                {
                "commentId": comment["commentId"],
                "text": ''.join([c['text'] for c in comment['contentText']['runs']]),
                "time": comment['publishedTimeText']['runs'][0]['text'],
                "likeCount": comment["likeCount"],
                'author': comment.get('authorText', {}).get('simpleText', ''),
                'channel': comment['authorEndpoint']['browseEndpoint']['browseId'],
                "authorIsChannelOwner": comment["authorIsChannelOwner"],
            },ignore_index=True)
            
        
        # load continuation tokens for next comments (ctoken & itct)
        continuation_tokens = [(next_cdata['continuation'], next_cdata['clickTrackingParams'])
                         for next_cdata in search_dict(comments_data, 'nextContinuationData')] + continuation_tokens
        time.sleep(0.1)


    ### df['time'] into datetime object
    df['time']= df['time'].apply(date_datetime)

 

    return df



        
if __name__ == '__main__':

    url = "https://www.youtube.com/watch?v=mKAEGSxwOAY&ab_channel=TheAIGuy"
    print(main(url))
    
            