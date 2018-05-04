from os import path

current_path = path.dirname(path.abspath(__file__))
parent_path = path.dirname(current_path)
db_path = path.join(parent_path, 'resources/twitter_database.db')
from data_methods.twitter_data_methods import twitter_database

db = twitter_database(db_path)
print(db.query("SELECT MIN(Date), MAX(Date), COUNT(*) FROM Tweets WHERE followers_count > 100000 \
                AND DATETIME(Date) >= '2018-04-23 09:00:00' AND DATETIME(Date) <= '2018-04-27 16:00:00'"))