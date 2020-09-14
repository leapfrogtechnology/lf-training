from sqlalchemy import (
    Table,
    Column,
    MetaData,
    UniqueConstraint
)
from sqlalchemy.dialects.mysql import (
    INTEGER,
    VARCHAR,
    FLOAT,
    ENUM
)

import mysql_db.config as config

if __name__ == "mysql_db.models":
    meta_data = MetaData()

    top_rated_movies = Table('top_rated_movies', meta_data,
                             Column('id', INTEGER(), primary_key=True),
                             Column('rank', INTEGER(), unique=True),
                             Column('title', VARCHAR(255)),
                             Column('release_year', INTEGER()),
                             Column('imdb_rating', FLOAT(2)),
                             mysql_engine=config.MYSQL_DB_ENGINE)

    top_rated_tv_shows = Table('top_rated_tv_shows', meta_data,
                               Column('id', INTEGER(), primary_key=True),
                               Column('rank', INTEGER(), unique=True),
                               Column('title', VARCHAR(255)),
                               Column('release_year', INTEGER()),
                               Column('imdb_rating', FLOAT(2)),
                               mysql_engine=config.MYSQL_DB_ENGINE)

    most_popular_movies = Table('most_popular_movies', meta_data,
                                Column('id', INTEGER(), primary_key=True),
                                Column('title', VARCHAR(255)),
                                Column('release_year', INTEGER()),
                                Column('imdb_rating', VARCHAR(255)),
                                Column('position', INTEGER()),
                                Column('pre_position', INTEGER()),
                                Column('popularity',
                                       ENUM("INCREASED", "DECREASED", "NO CHANGE")),
                                UniqueConstraint(
                                    "title", "release_year", "position"),
                                mysql_engine=config.MYSQL_DB_ENGINE)

    most_popular_tv_shows = Table('most_popular_tv_shows', meta_data,
                                  Column('id', INTEGER(), primary_key=True),
                                  Column('title', VARCHAR(255)),
                                  Column('release_year', INTEGER()),
                                  Column('imdb_rating', VARCHAR(255)),
                                  Column('position', INTEGER()),
                                  Column('pre_position', INTEGER()),
                                  Column('popularity',
                                         ENUM("INCREASED", "DECREASED", "NO CHANGE")),
                                  UniqueConstraint(
                                      "title", "release_year", "position"),
                                  mysql_engine=config.MYSQL_DB_ENGINE)
