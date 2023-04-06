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

# Twitter API credentials
twitter_api_key = "3hFqNeHA1hnonTYTnlxoSgImN"
twitter_api_secret = "Qvb9p37eH8vupKU0HpgHQDeCoDIDOuFJP4ukQY3Uo9luCzpV4X"
access_token = "301911063-SBkqkO40wrC2nDHIIdNYEJG2cc6S2mqlLxla1Jvi"
access_token_secret = "fEs8DQXEwG9H8ryDzpmGVl9M6matBjurelrvyxFTiZ1vh"
bear_token = "AAAAAAAAAAAAAAAAAAAAAGQamgEAAAAAM%2Bk2nL2cuNRiAbq0VOOx%2B2CPpak%3DWjcYhNTCLjinZd5Yq4vzlozpd0SoDIunNigHfHFzmDhRe3HRHL"


# Authenticate to Twitter
auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
api = tweepy.API(auth)

search_words = ["alpro", "activa", "actimel", "danette"]
date_since = "2023-01-01"
refined_tweets_list = []

for search_word in search_words:
    # # search tweets with the search_words and a limit of 200 tweets
    tweets = api.search_tweets(q=search_word, lang="en", tweet_mode="extended",
                               since=date_since, count=200)

    if not tweets:
        print("No tweets found")
        continue
    else:
        print(f"Got {len(tweets)} tweets for  {search_word}")

    for tweet in tweets:
        text = tweet.full_text

        refined_tweet = {"product": search_word,
                         "user": tweet.user.screen_name,
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
# df.to_excel(f'refined_tweets_{search_word}.xlsx', index=False)


# # # search tweets with the search_words and a limit of 200 tweets
# tweets = api.search_tweets(q=search_words, lang="en", tweet_mode="extended",
#                            since=date_since, count=100)

# print("No tweets found") if not tweets else print(f"Got {len(tweets)} tweets")

# refined_tweets_list = []
# for tweet in tweets:
#     text = tweet.full_text

#     refined_tweet = {"user": tweet.user.screen_name,
#                      'text': text,
#                      'sentiment': classifier(text)[0]['label'],
#                      'favorite_count': tweet.favorite_count,
#                      'retweet_count': tweet.retweet_count,
#                      'created_at': tweet.created_at,
#                      'link': f'https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}'}

#     refined_tweets_list.append(refined_tweet)

# df = pd.DataFrame(refined_tweets_list)
# df['created_at'] = pd.to_datetime(df['created_at'])
# # convert special characters to ascii
# df['text'] = df['text'].str.encode('ascii', 'ignore').str.decode('ascii')
# # df.to_csv('refined_tweets.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)
# df.to_excel('refined_tweets.xlsx', index=False)
