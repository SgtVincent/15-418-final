from os import path
import sys

current_path = path.dirname(path.abspath(__file__))
root_path = path.dirname(current_path)
sys.path.append(root_path)
from data_methods import twitter_data_methods as tm

# streaming config
tokens = {
    'access_token': "982333914201993216-3lUuCAaUCYgkB4kpkRz1tzL24veeYeX",
    'access_token_secret': "3XSDsJXSmUXwOwOlEflXYFTCXxIDOdhMQ4kNNzuTIRXkB",
    'consumer_key': "bz58HpjCEXS0kgn21Rj3qcvNo",
    'consumer_secret': "LjcezoypAs4Rjgmsd32bd8dB6tkGg7c6UvpIQ66hUi99EJYyPB"
}
track_path = path.join(root_path, 'resources/NASDQ100.txt')
with open(track_path, 'r') as f:
    stock_symbol = f.read()
    track = stock_symbol.split(",")

# filter config
tweet_filter = tm.key_word_filter(track)

# format config
tweet_formator = tm.twitter_format()

# database config
database_path = path.join(root_path, 'resources/twitter_database.db')
tweet_database = tm.twitter_database(database_path)

# start the pipeline
twitter_data_pipeline = tm.twitter_streaming(tokens, track, tweet_filter, tweet_formator, tweet_database)
twitter_data_pipeline.run()
