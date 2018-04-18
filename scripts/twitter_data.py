import sys
sys.path.append("..")
import twitter_crawler

# tokens
access_token = "982333914201993216-3lUuCAaUCYgkB4kpkRz1tzL24veeYeX"
access_token_secret = "3XSDsJXSmUXwOwOlEflXYFTCXxIDOdhMQ4kNNzuTIRXkB"
consumer_key = "bz58HpjCEXS0kgn21Rj3qcvNo"
consumer_secret = "LjcezoypAs4Rjgmsd32bd8dB6tkGg7c6UvpIQ66hUi99EJYyPB"

# config parameters
filename = '../resources/NASDQ100_tweets.json'
with open("../resources/NASDQ100.txt", 'r') as f:
    stock_symbol = f.read()
    track = stock_symbol.split(",")

# streaming data
t = twitter_crawler.TwitterStreaming(access_token, access_token_secret, consumer_key, consumer_secret)
t.get_data(filename, track)
