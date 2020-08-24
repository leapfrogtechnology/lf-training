import csv
import psycopg2

def create_table(cursor):
    cursor.execute("""
        CREATE TABLE weather(period text,descriptions text,temperature text)
    """)

def insert_data(cursor):
    with open('outputs/weather.csv', 'r') as file:
        data = csv.reader(file)
        next(data) 
        for row in data:
            cursor.execute("INSERT INTO weather VALUES (%s, %s, %s)",row)

def main():
    con = psycopg2.connect("host=localhost dbname=scraper user=scraper password=scraper")
    cursor = con.cursor()
    create_table(cursor)
    insert_data(cursor)
    con.commit()
    con.close()

if __name__ == "__main__":
    main()