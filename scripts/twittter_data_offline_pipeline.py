from os import path 
import sys
from data_methods import twitter_data_methods as tm

if __name__=='__main__':
    current_path = path.dirname(path.abspath(__file__))
    root_path = path.dirname(current_path)
    sys.path.append(root_path)
    twitter_path = "resource/NASDQ.json"
    fail_count = 0
    fail_idx = []
    with open(twitter_path, 'r') as f:
        for line in f:
            try:
                data = json.loads(data)
                if self.tweet_filter.filter(data):
                    data = self.tweet_formator.format(data)
                    self.tweet_db.insert_dict(data)
            except BaseException as e:
                print("Error on_data: %s" % str(e))
    print()
    with open("resource/fail_log.txt",'r') as f:
        f.write(str(fail_idx))
