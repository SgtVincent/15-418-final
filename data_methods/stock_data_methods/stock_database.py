import sqlite3


class stock_database:
    def __init__(self, db_path,
                 create_table_sql='''CREATE TABLE IF NOT EXISTS Nasdaq (
            Date DATETIME,
            Open FLOAT,
            High FLOAT,
            Low FLOAT,
            Close FLOAT,
            Volume FLOAT
            )'''):

        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table(create_table_sql)
        self.insert_count = 0

    def __del__(self):
        self.conn.commit()
        self.conn.close()
        print ("Nasdaq Database closed")

    def create_table(self, create_table_sql):
        self.cursor.execute(create_table_sql)

    # @row: list of data to be inserted
    def insert_row(
            self,
            row,
            table_name='Nasdaq',
            batch_mode=True
    ):

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

    # TODO: add execute_sql() method
    # input a sql
    # output some format, maybe data frame
