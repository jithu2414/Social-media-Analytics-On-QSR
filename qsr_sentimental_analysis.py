# -*- coding: utf-8 -*-
"""QSR_Sentimental analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rxDEbab0wRwRW6PCBzooU_g3O_Talwkq
"""

import sys
import tweepy 
import csv,re 
from textblob import TextBlob
import matplotlib.pyplot as plt

api = tweepy.API( wait_on_rate_limit=True)

class SentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def DownloadData(self): #input parameter search term is passed to the function in order to do particular task 
        # authenticating:identify this client and be sure that it is a valid account
        consumerKey = 'ui8rbyOADnvZQZCwAEJPg8hTZ'  #API key provided by twitter to identify our requests
        consumerSecret = 'jxIWFkzHiTANqSD4rIYHFmFE5Nw4czKkydVRTuUUqvEX0MeVyE' #password:Authorization provided to user by service provider
        accessToken = '1193971945764769793-sCKnrMI4zFyrUY20uK5IssFXGVgyZI' ##key used to retrieve the authorization information to the client
        accessTokenSecret = 'fzYut9SWq7ZbeIlJwuLYeoe370enzwktM4vQlHK0UtsgMy'
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret) # OAuthHandler:Authentication without using password to get connection
        auth.set_access_token(accessToken, accessTokenSecret) #You can throw these into a database, file, or where ever you store your data. To re-build an OAuthHandler from this stored access token
        api = tweepy.API(auth) #OAuthHandler equipped with an access token

        # input for term to be searched and how many tweets to search
        searchTerm = input("Enter Keyword/Tag to search about: ")
        NoOfTerms = int(input("Enter how many tweets to search: "))

        # searching for tweets
        self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms) #to check all the tweets with iphone as term or hashtag till the count of lines is 200

        # Open/create a file to append data to
        csvFile = open('iphone11.csv', 'w')

        # Use csv writer
        csvWriter = csv.writer(csvFile)


        # creating some variables to store info
        polarity = 0
        positive = 0
        wpositive = 0
        spositive = 0
        negative = 0
        wnegative = 0
        snegative = 0
        neutral = 0


        # iterating through tweets fetched
        for tweet in self.tweets:
            #Append to temp so that we can store in csv later. I use encode UTF-8
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            # print (tweet.text.translate(non_bmp_map))    #print tweet's text
            analysis = TextBlob(tweet.text)
            # print(analysis.sentiment)  # print tweet's polarity
            polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

            if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                neutral += 1
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                wpositive += 1
            elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                positive += 1
            elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                spositive += 1
            elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                wnegative += 1
            elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                negative += 1
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                snegative += 1


        # Write to csv and close csv file
        csvWriter.writerow(self.tweetText)
        csvFile.close()

        # finding average of how people are reacting
        positive = self.percentage(positive, NoOfTerms)
        wpositive = self.percentage(wpositive, NoOfTerms)
        spositive = self.percentage(spositive, NoOfTerms)
        negative = self.percentage(negative, NoOfTerms)
        wnegative = self.percentage(wnegative, NoOfTerms)
        snegative = self.percentage(snegative, NoOfTerms)
        neutral = self.percentage(neutral, NoOfTerms)

        # finding average reaction
        polarity = polarity / NoOfTerms

        # printing out data
        print("How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.")
        print()
        print("General Report: ")

        if (polarity == 0):
            print("Neutral")
        elif (polarity > 0 and polarity <= 0.3):
            print("Weakly Positive")
        elif (polarity > 0.3 and polarity <= 0.6):
            print("Positive")
        elif (polarity > 0.6 and polarity <= 1):
            print("Strongly Positive")
        elif (polarity > -0.3 and polarity <= 0):
            print("Weakly Negative")
        elif (polarity > -0.6 and polarity <= -0.3):
            print("Negative")
        elif (polarity > -1 and polarity <= -0.6):
            print("Strongly Negative")

        print()
        print("Detailed Report: ")
        print(str(positive) + "% people thought it was positive")
        print(str(wpositive) + "% people thought it was weakly positive")
        print(str(spositive) + "% people thought it was strongly positive")
        print(str(negative) + "% people thought it was negative")
        print(str(wnegative) + "% people thought it was weakly negative")
        print(str(snegative) + "% people thought it was strongly negative")
        print(str(neutral) + "% people thought it was neutral")

        self.plotpieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, NoOfTerms)


    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotpieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfSearchTerms):
        labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()



if __name__== "__main__": #to run the python file directly from command
    sa = SentimentAnalysis()
    sa.DownloadData()

import spacy

nlp = spacy.load("en_core_web_sm")
import numpy as np

import pandas as pd
ds=pd.read_csv("Burgerkinguk.csv",error_bad_lines=False)  #reading the comments csv file of particular phone
df=ds.iloc[:,:].values
df=np.array(df)
df=df.flatten()
l=[]
for i in df:
    doc = nlp(i)
    for token in doc:
        if  (token.pos_=="ADJ"):               #checking the words as adjectives
            l.append(token)
            
#converting data type from spacy.token to string
for i in range(0,len(l)):
    l[i]=str(l[i])

f=open("NNNNN_cloud.csv", "w+",encoding="UTF-8")             #opening files for saving cloud data
for i in l:
     f.write(i)
     f.write("\n")

     
f.close()