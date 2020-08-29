import sqlite3
import pandas
from pandas import DataFrame

con = sqlite3.connect('ScrapeData.db')
# Saves database in same location as this file
c = con.cursor()

c.execute('''CREATE TABLE MOVIE_RATINGS ([generated_id] INTEGER PRIMARY KEY, [TITLE] text, [RATING] float)''')

# Read data from the csv file
read_data = pandas.read_csv(r'output/topmovies.csv')
# Insert movie titles from csv file to the table
read_data.to_sql('MOVIE_RATINGS', con, if_exists = 'append', index = False)

for movies in con.execute("SELECT TITLE, RATING FROM MOVIE_RATINGS"):
    print(movies)

con.commit()
con.close()
