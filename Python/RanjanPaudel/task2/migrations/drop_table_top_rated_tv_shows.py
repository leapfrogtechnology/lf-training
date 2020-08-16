import sqlite3

imdb_movies_db = 'sqlite_dbs/imdb_movies.db'


def drop_table():
    connection = sqlite3.connect(imdb_movies_db)
    connection.execute('DROP TABLE top_rated_tv_shows')
    connection.commit()
    connection.close()


if __name__ == "__main__":
    drop_table()
