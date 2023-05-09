import sqlite3, pathlib

class ConnectDB:
    def __init__(self):
        path = str(pathlib.Path(__file__).parent.resolve())
        self.db = sqlite3.connect(path+'/database.db')
        self.db.row_factory = sqlite3.Row

    def insert(self, table, columns, values):
        c = ', '.join(columns)
        v = ', '.join(['?']*len(values))
        cur = self.db.cursor()
        cur.execute(f'INSERT INTO {table} ({c}) VALUES ({v})', values)
        self.db.commit()
        return cur.lastrowid
    
    def update(self, query, data):
        cur = self.db.cursor()
        cur.execute(query, data)
        self.db.commit()
        return cur.lastrowid
    
    def select(self, query):
        cur = self.db.cursor()
        cur.execute(query)
        datas = cur.fetchall()
        return datas

    def get_cursor(self):
        return self.db.cursor()

    def close(self):
        self.db.close()