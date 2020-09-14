import csv
import sqlite3

def create_table(cursor):
    cursor.execute("""
        CREATE TABLE weather(period text,descriptions text,temperature text)
    """)

def insert_data(path,cursor):
    insert = "INSERT INTO weather (period, descriptions, temperature)  \
    VALUES (?, ?, ?)"

    with open(path, 'r') as file:
        data = csv.DictReader(file)
        next(data) 
        for row in data:
            cursor.execute(insert, (row['period'],row['descriptions'],row['temperature']))


def main():
    path = './outputs/weather.csv'
    db = '/home/palson/db/scrapersqlite.db'
    con = sqlite3.connect(db)
    cursor = con.cursor()
    create_table(cursor)
    insert_data(path,cursor)
    con.commit()
    con.close()

if __name__ == "__main__":
    main()