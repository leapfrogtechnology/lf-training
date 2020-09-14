import os
from dotenv import load_dotenv
import sqlalchemy

load_dotenv()

_MYSQL_DB_HOST = os.getenv("MYSQL_DB_HOST")
_MYSQL_DB_PORT = os.getenv("MYSQL_DB_PORT")
_MYSQL_DB_USER = os.getenv("MYSQL_DB_USER")
_MYSQL_DB_PASSWORD = os.getenv("MYSQL_DB_PASSWORD")

import_paths = [
    "config",
    "mysql_db.config"
]

if import_paths.__contains__(__name__):
    engine = sqlalchemy.create_engine(
        f"mysql+mysqldb://{_MYSQL_DB_USER}:{_MYSQL_DB_PASSWORD}@{_MYSQL_DB_HOST}:{_MYSQL_DB_PORT}/imdb_movies"
    )

    MYSQL_DB_ENGINE = 'InnoDB'
