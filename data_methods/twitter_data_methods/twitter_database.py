from __future__ import print_function
import sqlite3


class twitter_database:
    def __init__(
            self,
            db_path,
            create_table_sql='''CREATE TABLE IF NOT EXISTS Tweets (
            Date DATETIME,
            text TEXT,
            followers_count INT,
            listed_count INT,
            statuses_count INT,
            friends_count INT,
            favourites_count INT
            )'''):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table(create_table_sql)
        self.insert_count = 0

    def __del__(self):
        self.conn.commit()
        self.conn.close()
        print("Tweets Database closed")

    def create_table(self, create_table_sql):
        self.cursor.execute(create_table_sql)

    def insert_dict(
            self,
            tweet,
            table_name='Tweets',
            keys=['Date', 'text', 'followers_count', 'listed_count', 'statuses_count',
                  'friends_count', 'favourites_count'],
            batch_mode=True
    ):
        row = [tweet[key] for key in keys]
        row_format = '(' + ','.join(['?'] * len(row)) + ')'
        self.cursor.execute('INSERT INTO %s VALUES %s' % (table_name, row_format), row)

        if not batch_mode:
            self.conn.commit()
            return

        self.insert_count += 1
        if self.insert_count % 10 == 0:
            self.conn.commit()
            self.insert_count = 0
            print("Commit 10000 inserts...")

    # query is a SQL format string
    # return a what
    def query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()