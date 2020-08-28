import sqlite3

conn = sqlite3.connect('output/results.db')
with conn:
    for row in conn.execute('SELECT * FROM data'):
        print(row)

conn.close()
