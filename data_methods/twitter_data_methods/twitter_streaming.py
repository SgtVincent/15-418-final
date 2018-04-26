# Import the necessary methods from tweepy library
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json


class _MyStreamListener(StreamListener):

    def __init__(self, tweet_filter, tweet_formator, tweet_db):
        super(_MyStreamListener, self).__init__()
        self.tweet_filter = tweet_filter
        self.tweet_formator = tweet_formator
        self.tweet_db = tweet_db

    def on_data(self, data):
        try:
            data = json.loads(data)
            if self.tweet_filter.filter(data):
                data = self.tweet_formator.format(data)
                self.tweet_db.insert_dict(data)
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


# This class provides twitter real time streaming data_methods
class twitter_streaming:

    def __init__(self, tokens, track, tweet_filter, tweet_formator, tweet_db):
        access_token = tokens['access_token']
        access_token_secret = tokens['access_token_secret']
        consumer_key = tokens['consumer_key']
        consumer_secret = tokens['consumer_secret']
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.track = track
        self.twitter_stream = Stream(auth, _MyStreamListener(tweet_filter=tweet_filter,
                                                             tweet_formator=tweet_formator, tweet_db=tweet_db))

    def run(self):
        while True:
            try:
                self.twitter_stream.filter(track=self.track, languages=["en"])
            except:
                continue
