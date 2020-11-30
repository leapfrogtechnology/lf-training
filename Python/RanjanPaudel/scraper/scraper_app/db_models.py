from sqlalchemy import (
    Table,
    Column,
    MetaData,
    UniqueConstraint,
    ForeignKey,
    text
)
from sqlalchemy.dialects.mysql import (
    INTEGER,
    VARCHAR,
    FLOAT,
    ENUM,
    DATE,
    TIMESTAMP,
    TEXT
)
from sqlalchemy.engine import Connection
from sqlalchemy.sql import Select, Delete, Update
from datetime import datetime

import scraper_app.db_config as db_config

meta_data = MetaData()

users = Table('users', meta_data,
              Column('id', INTEGER(), primary_key=True),
              Column('full_name', VARCHAR(100), nullable=False),
              Column('username', VARCHAR(100),
                     unique=True, nullable=False),
              Column('dob', DATE, nullable=False),
              Column('password', VARCHAR(255), nullable=False),
              Column('created_at', TIMESTAMP(),
                     nullable=False, server_default=text('CURRENT_TIMESTAMP')),
              mysql_engine=db_config.MYSQL_DB_ENGINE)

refresh_tokens = Table('refresh_tokens', meta_data,
                       Column('id', INTEGER(), primary_key=True),
                       Column('user_id', INTEGER(), ForeignKey(
                           'users.id'), nullable=False),
                       Column('refresh_token', TEXT, nullable=False),
                       mysql_engine=db_config.MYSQL_DB_ENGINE)

top_rated_movies = Table('top_rated_movies', meta_data,
                         Column('id', INTEGER(), primary_key=True),
                         Column('rank', INTEGER(), unique=True),
                         Column('title', VARCHAR(255)),
                         Column('release_year', INTEGER()),
                         Column('imdb_rating', FLOAT(2)),
                         Column('img_link', VARCHAR(255)),
                         Column('imdb_link', VARCHAR(255)),
                         mysql_engine=db_config.MYSQL_DB_ENGINE)

top_rated_tv_shows = Table('top_rated_tv_shows', meta_data,
                           Column('id', INTEGER(), primary_key=True),
                           Column('rank', INTEGER(), unique=True),
                           Column('title', VARCHAR(255)),
                           Column('release_year', INTEGER()),
                           Column('imdb_rating', FLOAT(2)),
                           Column('img_link', VARCHAR(255)),
                           Column('imdb_link', VARCHAR(255)),
                           mysql_engine=db_config.MYSQL_DB_ENGINE)

most_popular_movies = Table('most_popular_movies', meta_data,
                            Column('id', INTEGER(), primary_key=True),
                            Column('title', VARCHAR(255)),
                            Column('release_year', INTEGER()),
                            Column('imdb_rating', VARCHAR(255)),
                            Column('position', INTEGER()),
                            Column('pre_position', INTEGER()),
                            Column('popularity',
                                   ENUM("INCREASED", "DECREASED", "NO CHANGE")),
                            Column('img_link', VARCHAR(255)),
                            Column('imdb_link', VARCHAR(255)),
                            UniqueConstraint(
                                "title", "release_year", "position"),
                            mysql_engine=db_config.MYSQL_DB_ENGINE)

most_popular_tv_shows = Table('most_popular_tv_shows', meta_data,
                              Column('id', INTEGER(), primary_key=True),
                              Column('title', VARCHAR(255)),
                              Column('release_year', INTEGER()),
                              Column('imdb_rating', VARCHAR(255)),
                              Column('position', INTEGER()),
                              Column('pre_position', INTEGER()),
                              Column('popularity',
                                     ENUM("INCREASED", "DECREASED", "NO CHANGE")),
                              Column('img_link', VARCHAR(255)),
                              Column('imdb_link', VARCHAR(255)),
                              UniqueConstraint(
                                  "title", "release_year", "position"),
                              mysql_engine=db_config.MYSQL_DB_ENGINE)

movie_list_meta = Table('movie_list_meta', meta_data,
                        Column('id', INTEGER(), primary_key=True),
                        Column('list_name', ENUM("top_rated_movies", "top_rated_tv_shows",
                                                 "most_popular_movies", "most_popular_tv_shows"), unique=True, nullable=False),
                        Column('last_updated', TIMESTAMP()),
                        mysql_engine=db_config.MYSQL_DB_ENGINE)


conn = Connection(db_config.engine)
tables = meta_data.tables


def create_user(user_data):
    result = ''
    with conn.begin():
        user_stmt = users.insert().values(user_data)
        result = conn.execute(user_stmt)

    return result


def find_user_by_username(username):
    result = []
    with conn.begin():
        user_stmt = Select([users]).where(users.c.username == username)
        for row in conn.execute(user_stmt):
            result.append(dict(row))

    return result


def find_user_by_id(user_id):
    result = []
    with conn.begin():
        user_stmt = Select([users]).where(users.c.id == user_id)
        for row in conn.execute(user_stmt):
            result.append(dict(row))

    return result


def check_user_existance(username):
    result = find_user_by_username(username)
    if len(result) > 0:
        return True

    return False


def create_token(user, refresh_token):
    new_token = {
        "user_id": user['id'],
        "refresh_token": refresh_token
    }

    result = ''
    with conn.begin():
        token_stmt = refresh_tokens.insert().values(new_token)
        result = conn.execute(token_stmt)

    return result


def find_token(user):
    result = []
    with conn.begin():
        token_stmt = Select([refresh_tokens]).where(
            refresh_tokens.c.user_id == user['id'])
        for row in conn.execute(token_stmt):
            result.append(dict(row))

    return result


def update_token(user, old_token, new_token):
    result = ''
    with conn.begin():
        token_stmt = refresh_tokens.update().where(refresh_tokens.c.user_id == user['id']).where(
            refresh_tokens.c.refresh_token == old_token).values(
            refresh_token=new_token)
        result = conn.execute(token_stmt)

    return result


def remove_token(user):
    result = ''
    with conn.begin():
        token_stmt = refresh_tokens.delete().where(
            refresh_tokens.c.user_id == user['id'])
        result = conn.execute(token_stmt)

    return result


def create_movie_list(table_name, movie_list):
    result = ''
    with conn.begin():
        list_stmt = tables[table_name].insert().values(movie_list)
        result = conn.execute(list_stmt)

    return result


def update_movie_list(table_name, movie_list):
    result = ''
    with conn.begin():
        remove_all_stmt = tables[table_name].delete()
        conn.execute(remove_all_stmt)
        insert_many_stmt = tables[table_name].insert().values(movie_list)
        result = conn.execute(insert_many_stmt)

    return result


def update_movie_meta(list_name):
    result = ''
    with conn.begin():
        update_stmt = movie_list_meta.update().where(movie_list_meta.c.list_name ==
                                                     list_name).values(last_updated=datetime.utcnow())
        result = conn.execute(update_stmt)

    return result


def find_movie_meta(list_name):
    result = []
    with conn.begin():
        stmt = movie_list_meta.select().where(movie_list_meta.c.list_name == list_name)
        for row in conn.execute(stmt):
            result.append(dict(row))

    return result[0]


def find_all_movies(table_name):
    result = []
    with conn.begin():
        list_stmt = tables[table_name].select()
        for row in conn.execute(list_stmt):
            result.append(dict(row))

    return result
