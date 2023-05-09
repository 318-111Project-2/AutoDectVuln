import sqlite3, pathlib

path = str(pathlib.Path(__file__).parent.resolve())

connection = sqlite3.connect(path+'/database.db')

with open(path+'/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

connection.commit()
connection.close()