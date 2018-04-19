# Import the necessary methods from tweepy library
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener, json


class _MyStreamListener(StreamListener):
    file_path = ''

    def __init__(self, file_path):
        super(_MyStreamListener, self).__init__()
        self.file_path = file_path

    def on_data(self, data):
        try:
            with open(self.file_path, 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


# This class provides twitter real time streaming data
class TwitterStreaming:
    access_token = ''
    access_token_secret = ''
    consumer_key = ''
    consumer_secret = ''

    def __init__(self, access_token, access_token_secret, consumer_key, consumer_secret):
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

    def get_data(self, file_path, track, follow=None):
        auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        twitter_stream = Stream(auth, _MyStreamListener(file_path))
        while True:
            try:
                twitter_stream.filter(track=track, follow=follow, languages=["en"])
            except:
                continue
