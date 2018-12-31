#!/usr/bin/env python

import pandas as pd
import twitter
from textblob import TextBlob
import re
import os
class Artist:

  CONSUMER_KEY=os.environ["CONSUMER_KEY"]
  CONSUMER_SECRET=os.environ[ "CONSUMER_SECRET" ]
  ACCESS_TOKEN_KEY=os.environ[ "ACCESS_TOKEN_KEY" ]
  ACCESS_TOKEN_SECRET=os.environ[ "ACCESS_TOKEN_SECRET" ]

  __api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_TOKEN_KEY,
                      access_token_secret=ACCESS_TOKEN_SECRET)

  def __init__(self, name):
    self.name = name
    self.albums = []
    self.__df = pd.DataFrame(columns=['user', 'location', 'sentiment', 'followers','retweets'])

  # Returns an Array of dictionaries where the location is available
  def search_twitter(self):
    response = self.__api.GetSearch(term=self.name, count=100)
    ret = []
    for r in response:
      d = r.AsDict()
      if 'location' in d['user'].keys():
        ret.append(d)
    return ret

  # Gets rid of unnecessary characters.
  def __clean_tweet(self, tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

  # Scores tweet's sentiment
  def get_tweet_sentiment(self, tweet):
    analysis = TextBlob(self.__clean_tweet(tweet))
    print(analysis.sentiment.polarity)
    if analysis.sentiment.polarity > 0:
      return 'positive'
    elif analysis.sentiment.polarity == 0:
      return 'neutral'
    else:
      return 'negative'


  def store_data(self, arr):
    pass





drake = Artist('Drake')
print(drake.search_twitter())

