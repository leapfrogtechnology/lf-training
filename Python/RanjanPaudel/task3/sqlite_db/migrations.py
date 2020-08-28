import sqlite3

imdb_movies_db = 'sqlite_db/imdb_movies.db'


def create_table_most_popular_movies():
    with sqlite3.connect(imdb_movies_db) as connection:
        connection.execute('''CREATE TABLE IF NOT EXISTS most_popular_movies
                            (id INTEGER PRIMARY KEY ASC, 
                            title TEXT, 
                            release_year INTEGER, 
                            imdb_rating TEXT, 
                            position INTEGER, 
                            pre_position INTEGER,
                            popularity TEXT,
                            UNIQUE(title, release_year, position))
                        ''')
        connection.commit()
    print('Table most_popular_movies created')


def create_table_most_popular_tv_shows():
    with sqlite3.connect(imdb_movies_db) as connection:
        connection.execute('''CREATE TABLE IF NOT EXISTS most_popular_tv_shows
                            (id INTEGER PRIMARY KEY ASC, 
                            title TEXT, 
                            release_year INTEGER, 
                            imdb_rating TEXT, 
                            position INTEGER, 
                            pre_position INTEGER,
                            popularity TEXT,
                            UNIQUE(title, release_year, position))
                        ''')
        connection.commit()
    print('Table most_popular_tv_shows created')


def create_table_top_rated_movies():
    with sqlite3.connect(imdb_movies_db) as connection:
        connection.execute('''CREATE TABLE IF NOT EXISTS top_rated_movies
                            (id INTEGER PRIMARY KEY ASC, 
                            rank INTEGER UNIQUE, 
                            title TEXT, 
                            release_year INTEGER, 
                            imdb_rating REAL)
                        ''')
        connection.commit()
    print('Table top_rated_movies created')


def create_table_top_rated_tv_shows():
    with sqlite3.connect(imdb_movies_db) as connection:
        connection.execute('''CREATE TABLE IF NOT EXISTS top_rated_tv_shows
                            (id INTEGER PRIMARY KEY ASC, 
                            rank INTEGER UNIQUE, 
                            title TEXT, 
                            release_year INTEGER, 
                            imdb_rating REAL)
                        ''')
        connection.commit()
    print('Table top_rated_tv_shows created')


def drop_table_most_popular_movies():
    with sqlite3.connect(imdb_movies_db) as connection:
        connection.execute('DROP TABLE most_popular_movies')
        connection.commit()
    print('Table most_popular_movies dropped.')


def drop_table_most_popular_tv_shows():
    with sqlite3.connect(imdb_movies_db) as connection:
        connection.execute('DROP TABLE most_popular_tv_shows')
        connection.commit()
    print('Table most_popular_tv_shows dropped.')


def drop_table_top_rated_movies():
    with sqlite3.connect(imdb_movies_db) as connection:
        connection.execute('DROP TABLE top_rated_movies')
        connection.commit()
    print('Table top_rated_movies dropped.')


def drop_table_top_rated_tv_shows():
    with sqlite3.connect(imdb_movies_db) as connection:
        connection.execute('DROP TABLE top_rated_tv_shows')
        connection.commit()
    print('Table top_rated_tv_shows dropped.')


if __name__ == "sqlite_db.migrations":
    def create_all():
        create_table_top_rated_movies()
        create_table_top_rated_tv_shows()
        create_table_most_popular_movies()
        create_table_most_popular_tv_shows()

    def drop_all():
        drop_table_top_rated_movies()
        drop_table_top_rated_tv_shows()
        drop_table_most_popular_movies()
        drop_table_most_popular_tv_shows()
