import sqlite3

top_rated_db = 'sqlite_db/imdb_movies.db'

table_all_columns = {
    "top_rated_movies": "(rank, title, release_year, imdb_rating)",
    "most_popular_movies": "(title, release_year, imdb_rating, position, pre_position, popularity)",
    "top_rated_tv_shows": "(rank, title, release_year, imdb_rating)",
    "most_popular_tv_shows": "(title, release_year, imdb_rating, position, pre_position, popularity)"
}

table_all_column_binds = {
    "top_rated_movies": "(?, ?, ?, ?)",
    "most_popular_movies": "(?, ?, ?, ?, ?, ?)",
    "top_rated_tv_shows": "(?, ?, ?, ?)",
    "most_popular_tv_shows": "(?, ?, ?, ?, ?, ?)"
}


def genarate_tuple_list(dict_list):
    tuple_list = []
    for _dict in dict_list:
        tuple_list.append(tuple(_dict.values()))

    return tuple_list


def dict_factory(cursor, row):
    row_dict = {}
    for idx, col in enumerate(cursor.description):
        row_dict[col[0]] = row[idx]

    return row_dict


if __name__ == "sqlite_handler":
    def insert_many(table_name, dict_list):
        tuple_list = genarate_tuple_list(dict_list)

        with sqlite3.connect(top_rated_db) as conn:
            conn.executemany(f'''
                    INSERT INTO {table_name} {table_all_columns[table_name]} VALUES{table_all_column_binds[table_name]}
            ''', tuple_list)

            conn.commit()

    def fetch_all(table_name):
        dict_list = []
        with sqlite3.connect(top_rated_db) as conn:
            conn.row_factory = dict_factory
            cur = conn.cursor()

            for row in cur.execute(f'SELECT * FROM {table_name}'):
                dict_list.append(row)

        return dict_list
