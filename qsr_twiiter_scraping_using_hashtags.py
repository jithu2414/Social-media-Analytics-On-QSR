# -*- coding: utf-8 -*-
"""QSR - Twiiter scraping using hashtags.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1K9q6wpD5OWo0agJaHxSpaJhIdzl0Q3lL
"""

#Twitter Comments Scrapper

import tweepy

from nlppreprocess import NLP

obj=NLP()

term_or_hashtag='#burgerking'             #change the name of phone in hastag

f= open("burgerking.csv","w+",encoding="UTF-8")    #opening particualr file for different phones
def DownloadData(searchTerm):
        # authenticating
        consumerKey = '667OOi8BcK8R2gNOJNecmuOra'
        consumerSecret = 'Wxhhv1dH5TAyrtBVKBjNg52vGyzL3YGbYRVGkZ0ChfFpsXJyR6'
        accessToken = '1193971945764769793-sCKnrMI4zFyrUY20uK5IssFXGVgyZI'
        accessTokenSecret = 'fzYut9SWq7ZbeIlJwuLYeoe370enzwktM4vQlHK0UtsgM'
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)

        
        
        NoOfTerms = 2000                     #change number of comments you want

        # searching for tweets
        tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)
        for i in tweets:
            text=obj.process(i.text)
            f.write(text)
            f.write('\n')
        
if __name__ == '__main__':
    DownloadData(term_or_hashtag)