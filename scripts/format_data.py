from os import path
current_path = path.dirname(path.abspath(__file__))
root_path = path.dirname(current_path)
resource_path = path.join(root_path, "resources")
filename = "filtered_tweets.json"
file_path = path.join(resource_path, filename)
result_path = path.join(resource_path, 'formatted_tweets.json')
from data.data_preprocessor.twitter_formator import *

count = 0
with open(file_path, 'r') as f:
    with open(result_path, 'w') as g:
        for line in f:
            count += 1
            if (count % 10000) == 0:
                count = 0
                print("still working!")
            g.write(twitter_format(line) + '\n')
