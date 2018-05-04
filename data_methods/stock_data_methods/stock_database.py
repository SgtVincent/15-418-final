import sqlite3


class stock_database:
    def __init__(self, db_path):
        self.row_format = " (Date DATETIME, Open FLOAT, High FLOAT, Low FLOAT, Close FLOAT, Volume FLOAT)"
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.insert_count = 0

    def __del__(self):
        self.conn.commit()
        self.conn.close()
        print ("Nasdaq Database closed")

    def create_table(self, table_name):
        create_table_sql = "CREATE TABLE IF NOT EXISTS " + table_name + self.row_format
        self.cursor.execute(create_table_sql)

    # @row: list of data to be inserted
    def insert_row(self, row, table_name, batch_mode=True):

        row_format = '(' + ','.join(['?'] * len(row)) + ')'
        self.cursor.execute('INSERT INTO %s VALUES %s' % (table_name, row_format), row)

        if not batch_mode:
            self.conn.commit()
            return

        self.insert_count += 1
        if self.insert_count % 10000 == 0:
            self.conn.commit()
            self.insert_count = 0
            print ("Commit 10000 inserts...")

    # query is a SQL format string
    # return a list of row(tuple)
    def query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
