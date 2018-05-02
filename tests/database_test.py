from os import path

current_path = path.dirname(path.abspath(__file__))
parent_path = path.dirname(current_path)
db_path = path.join(parent_path, 'resources/twitter_database.db')
from data_methods.twitter_data_methods import twitter_database

db = twitter_database(db_path)
print(db.query("SELECT * FROM Tweets")[0][2])
