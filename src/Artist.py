#!/usr/bin/env python

import pandas as pd
import twitter
from textblob import TextBlob
import re
import os
import string

class Artist:
  #TODO If i change whats storing into dataframe I must change the dataframe as well.
  # If i change sentiment to a number, must change datframe as well.
  __path = "./data/"

  CONSUMER_KEY=os.environ["CONSUMER_KEY"]
  CONSUMER_SECRET=os.environ[ "CONSUMER_SECRET" ]
  ACCESS_TOKEN_KEY=os.environ[ "ACCESS_TOKEN_KEY" ]
  ACCESS_TOKEN_SECRET=os.environ[ "ACCESS_TOKEN_SECRET" ]

  __api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_TOKEN_KEY,
                      access_token_secret=ACCESS_TOKEN_SECRET)

  __columns =['user', 'location', 'text', 'sentiment', 'followers','retweets', 'favorites']

  def __init__(self, name, handle):
    self.handle = handle
    self.name = name
    self.albums = []
    self.file_name = name + '_data.csv'
    try:
      self.__df = pd.read_csv(self.__path + self.file_name)
    except IOError:
      self.__df = pd.DataFrame(columns=self.__columns)

  # Returns an Array of dictionaries where the location is available
  def search_twitter(self):
    # TODO Chance count back to 100 once i get a reliable way to extract multiple tweets
    # and put into the dataframe
    response = self.__api.GetSearch(term=self.name, count=10)
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
    if analysis.sentiment.polarity > 0:
      return 'positive'
    elif analysis.sentiment.polarity == 0:
      return 'neutral'
    else:
      return 'negative'


  #'user', 'location', 'text', 'sentiment', 'followers','retweets']
  def store_data(self):
    arr = self.search_twitter()
    # Iterate through dictionary and append rows
    for d in arr:
      new_dict = {'text': d['text'], 'location':d['user']['location'],
          'retweets': d.get( 'retweet_count' ),
          'followers': d['user']['followers_count'],
          'user': d['user']['name'], 'sentiment': self.get_tweet_sentiment(d['text']),
          'favorites': d['user']['favourites_count']}
      self.__df = self.__df.append(pd.Series(new_dict), ignore_index=True)
    self.__df.replace({r'[^\x00-\x7F]+':''}, regex=True, inplace=True)
    self.__df = self.__df.loc[:, ~self.__df.columns.str.contains('^Unnamed')]
    self.__df.drop_duplicates(subset=['user', 'text'], inplace=True)
    self.__df.reset_index(drop=True, inplace=True)
    # Output to .csv
    self.__df.to_csv(self.__path + self.file_name)

  def reset_dataframe(self):
    self.__df = pd.DataFrame(columns=self.__columns)


drake = Artist('Drake', '@Drake')
drake.reset_dataframe()
drake.store_data()


