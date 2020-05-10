# -*- coding: utf-8 -*-
"""
Created on Sat May  9 21:54:16 2020

@author: Kareem Felfel
Sentiment analysis program that uses tweets fetched from twitter using python
to represent the data in different forms. Program focuses on visualization and
interpretation of the data gathered from ones twitter account.
"""
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import re
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

def main():
    APIKey = "PUT YOUR API KEY HERE"
    APISecret = "PUT YOUR API SECRET HERE"
    AccessToken = "PUT YOUR ACCESS TOKEN HERE"
    ATSecret = "PUT YOUR ACCESS TOKEN SECRET HERE"
    
    ''' Authentication Object '''
    Authenticate = tweepy.OAuthHandler(APIKey, APISecret)
    
    ''' Set Access Token and Secret '''
    Authenticate.set_access_token(AccessToken, ATSecret)
    
    ''' Create API Object with Auth information '''
    api = tweepy.API(Authenticate, wait_on_rate_limit = True)    
    
    ''' Successfull message '''
    print("Tokens worked successfully, you're inside twitter.")
    TwitterAccount = input("What account are you looking to extract information from? ")
    numTweets = int(input("How many Tweets are you extracting from this account? (MAX 200 TWEETS) "))
    posts = api.user_timeline(TwitterAccount, count = numTweets, lang = 'en',
                              tweet_mode = "extended")
    RecentTweets = input("Would you like to check the recent 5 tweets? (y/n) ")
    if RecentTweets in ["y","Y"]:
        print("5 recent tweets: \n")
        i = 1
        for tweet in posts[0:5]:
            print(str(i) + ') ' + tweet.full_text + '\n')
            i+=1
            
    '''Create DataFrame of Tweets '''
    df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])
    
    
    #call clean text to clean the data frame
    df['Tweets'] = df['Tweets'].apply(cleanText)
    #Dataframe of subjectivity
    df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
    df['Polarity'] = df['Tweets'].apply(getPolarity)
    df['Analysis'] = df['Polarity'].apply(getAnalysis)
    
    ''' WordCloud '''
    boolWC = input("Would you like to visualize the most common words in wordCloud? (y/n) ")
    if boolWC in ['y', "Y"]:
        AllWords = ' '.join( [tweets for tweets in df['Tweets']] )
        wordCloud = WordCloud(width = 800, height = 500, random_state = 21,
                              max_font_size = 119,
                              background_color = "white").generate(AllWords)
        plt.imshow(wordCloud, interpolation = 'bilinear')
        plt.axis('off')
        plt.show()
        
    ''' Scatter Plot '''
    PnSBool = input("Would you like to view the polarity and subjectivity data visualized in Scatter Plot? (y/n) ")
    if PnSBool in ['y', "Y"]:
        plt.figure(figsize = (8,6))
        for i in range(0, df.shape[0]):
            plt.scatter(df['Polarity'][i], df['Subjectivity'][i], color = "Blue")
        plt.title("Sentiment Analysis of Polarity and Subjectivity")
        plt.xlabel("Polarity")
        plt.ylabel("Subjectivity")
        plt.show()
    ''' Percentages '''
    #Percentage of Positive tweets
    ptweets = df[df.Analysis == "Positive"]
    ptweets = ptweets['Tweets']
    PositiveTweets = round((ptweets.shape[0] / df.shape[0])*100, 1)
    
    #Percentage of negative tweets
    ntweets = df[df.Analysis == "Negative"]
    ntweets = ntweets ['Tweets']
    NegativeTweets = round((ntweets.shape[0] / df.shape[0])*100, 1)
    df["Analysis"].value_counts()
    
    PieBool = input ("Would you like to view the visualization of positive, neutral, and negative tweets? (y/n) ")
    if PieBool in ["y", "Y"]:
        plt.title("Positive, Negative, and Neutral Tweets")
        titles = ["Positive", "Negative", "Neutral"]
        percentages = [PositiveTweets, NegativeTweets, 100-(PositiveTweets + NegativeTweets)]
        plt.pie(percentages, labels = titles, autopct = "%0.1f%%", radius = 1.1, startangle = 180)
        plt.show()
        #print("Positive: " + str(PositiveTweets))
        #print("Negative: " + str(NegativeTweets))
        
    
       
        
    
#Function that cleans text taken from the data frame    
def cleanText(text):
    # Clean out any mentions in tweet
    text = re.sub(r"@[A-Za-z0-9]+", '', text)
    # clean out any hashtags in tweet
    text = re.sub(r"#", '', text)
    #Clean out any retweet
    text = re.sub(r"RT[\s]+", '', text)
    # clean out any links
    text = re.sub(r"https?:\/\/\S+", '', text)
    
    return text
# function that gets the subjectivity of each tweet and store it in the df              
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity
# returns how positive or negative a tweet is
def getPolarity(text):
    return TextBlob(text).sentiment.polarity   
#get negative, neutral, and positive analysis
def getAnalysis(score):
    if score < 0:
        return "Negative"
    elif score == 0:
        return "Neutral"
    else:
        return "Positive"
    
main()
