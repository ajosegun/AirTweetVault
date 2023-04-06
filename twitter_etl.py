import csv
import tweepy
import pandas as pd
import json
from datetime import datetime
import s3fs
import config
from transformers import pipeline

# Load the sentiment analysis pipeline
classifier = pipeline("sentiment-analysis",
                      model="cardiffnlp/twitter-roberta-base-sentiment-latest")

# # Twitter API credentials
twitter_api_key = config.twitter_api_key
twitter_api_secret = config.twitter_api_key
access_token = config.access_token
access_token_secret = config.access_token_secret
bear_token = config.bear_token

# Authenticate to Twitter
auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
# , wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
api = tweepy.API(auth)

# # # Creating an API object
# tweets = api.user_timeline(screen_name='@elonmusk',
#                            # 200 is the maximum allowed count
#                            count=200,
#                            include_rts=False,
#                            # Necessary to keep full_text
#                            # otherwise only the first 140 words are extracted
#                            tweet_mode='extended'
#                            )

search_words = "alpro"  # activa actimel danette"
date_since = "2023-01-01"

# # search tweets with the search_words and a limit of 200 tweets
tweets = api.search_tweets(q=search_words, lang="en",
                           since=date_since, count=200)

# api.search_tweets(q=search_words, lang="en", since=date_since)
# print(tweets[0])
# Collect tweets
# tweets = tweepy.Cursor(api.search_tweets, q=search_words,
#                        lang="en", since=date_since).items(200)

print(f"Got {len(tweets)} tweets")

refined_tweets_list = []
for tweet in tweets:
    text = tweet._json["text"]

    refined_tweet = {"user": tweet.user.screen_name,
                     'text': text,
                     'sentiment': classifier(text)[0]['label'],
                     'favorite_count': tweet.favorite_count,
                     'retweet_count': tweet.retweet_count,
                     'created_at': tweet.created_at,
                     'link': f'https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}'}

    refined_tweets_list.append(refined_tweet)

df = pd.DataFrame(refined_tweets_list)
df['created_at'] = pd.to_datetime(df['created_at'])
# convert special characters to ascii
df['text'] = df['text'].str.encode('ascii', 'ignore').str.decode('ascii')
df.to_csv('refined_tweets.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)

# Create a tweet list as follows:
# tweets = []

# # Define the search term and the date_since date as variables
# search_words = "#covid19"
# date_since = "2020-01-01"

# # Collect tweets
# tweets = tweepy.Cursor(api.search, q=search_words,
#                        lang="en", since=date_since).items(1000)

# # Iterate and print tweets
# for tweet in tweets:
#     print(tweet.text)

# # Iterate and store tweets in a list
# tweets = []
# for tweet in tweepy.Cursor(api.search, q=search_words, lang="en", since=date_since).items(1000):
#     tweets.append(tweet)
