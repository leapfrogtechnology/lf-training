import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

_MYSQL_DB_HOST = os.getenv("MYSQL_DB_HOST")
_MYSQL_DB_PORT = os.getenv("MYSQL_DB_PORT")
_MYSQL_DB_USER = os.getenv("MYSQL_DB_USER")
_MYSQL_DB_PASSWORD = os.getenv("MYSQL_DB_PASSWORD")

engine = create_engine(
    f"mysql+mysqldb://{_MYSQL_DB_USER}:{_MYSQL_DB_PASSWORD}@{_MYSQL_DB_HOST}:{_MYSQL_DB_PORT}/scraper_app")

MYSQL_DB_ENGINE = 'InnoDB'
