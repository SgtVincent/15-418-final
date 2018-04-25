import time
import sqlite3
import json

def ConvertTime(t_time): 
    return time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(t_time,'%a %b %d %H:%M:%S +0000 %Y'))

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

def InsertTweet(cursor, row,):
    cursor.execute('INSERT INTO Tweets VALUES (?,?,?,?,?,?,?)',row)




#file_path = "../resources/formated_tweets.json"
file_path = "test_json.json"
database_path = "db_test.db"

conn = sqlite3.connect(database_path)
cursor = conn.cursor()
CreateTable(cursor)


with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        js = json.loads(line)
        row = [js['Date'],js['text'],js['followers_count'],js['listed_count'],js['statuses_count'],js['friends_count'], js['favourites_count']]
        InsertTweet(cursor, row)

