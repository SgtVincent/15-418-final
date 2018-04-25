import time
import sqlite3
import json
from os import path

current_path = path.dirname(path.abspath(__file__))
root_path = path.dirname(path.dirname(current_path))
resource_path = path.join(root_path, "resources/")


def CreateTable(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS Tweets (
        Date DATETIME,
        text TEXT,
        followers_count INT,
        listed_count INT,
        statuses_count INT,
        friends_count INT,
        favourites_count INT
        )''')


def InsertTweet(cursor, row):
    b = cursor.execute('INSERT INTO Tweets VALUES (?,?,?,?,?,?,?)', row)
    x = 1


file_path = path.join(resource_path, "formatted_tweets.json")
database_path = path.join(resource_path, "tweets.db")
conn = sqlite3.connect(database_path)
cursor = conn.cursor()
CreateTable(cursor)

count = 0
with open(file_path, 'r') as f:
    for line in f:
        count += 1
        js = json.loads(line)
        row = [js['Date'], js['text'], js['followers_count'], js['listed_count'], js['statuses_count'],
               js['friends_count'], js['favourites_count']]
        InsertTweet(cursor, row)

for row in cursor.execute("SELECT * FROM Tweets"):
    print(row)