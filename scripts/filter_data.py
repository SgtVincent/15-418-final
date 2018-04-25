# some test
from os import path
import json
import sys
current_path = path.dirname(path.abspath(__file__))
root_path = path.dirname(current_path)
resource_path = path.join(root_path, "resources")
sys.path.append(resource_path)
from data.data_preprocessor.twitter_filter import *

twitter_path = path.join(resource_path, "NASDQ100_tweets.json")
match_path = path.join(resource_path, "NASDQ100.txt")
result_path = path.join(resource_path, 'filtered_tweets.json')
key_words = file2key_words(match_path, ',')
my_filter = key_word_filter(key_words)

with open(twitter_path, 'r') as f:
    with open(result_path, 'w') as g:
        for line in f:
            twitter = json.loads(line)
            if my_filter.filter_in_text(twitter):
                g.write(line)
