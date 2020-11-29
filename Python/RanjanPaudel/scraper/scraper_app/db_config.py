import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

_MYSQL_DB_HOST = os.getenv("MYSQL_DB_HOST")
_MYSQL_DB_PORT = os.getenv("MYSQL_DB_PORT")
_MYSQL_DB_USER = os.getenv("MYSQL_DB_USER")
_MYSQL_DB_PASSWORD = os.getenv("MYSQL_DB_PASSWORD")

_MYSQL_TEST_DB_HOST = os.getenv("MYSQL_TEST_DB_HOST")
_MYSQL_TEST_DB_PORT = os.getenv("MYSQL_TEST_DB_PORT")
_MYSQL_TEST_DB_USER = os.getenv("MYSQL_TEST_DB_USER")
_MYSQL_TEST_DB_PASSWORD = os.getenv("MYSQL_TEST_DB_PASSWORD")

app_env = os.environ['FLASK_ENV']
engine = ''

print('APP ENV: ', app_env)

if app_env == 'development':
    engine = create_engine(
        f"mysql+mysqldb://{_MYSQL_DB_USER}:{_MYSQL_DB_PASSWORD}@{_MYSQL_DB_HOST}:{_MYSQL_DB_PORT}/scraper_app")

if app_env == 'test':
    engine = create_engine(
        f"mysql+mysqldb://{_MYSQL_TEST_DB_USER}:{_MYSQL_TEST_DB_PASSWORD}@{_MYSQL_TEST_DB_HOST}:{_MYSQL_TEST_DB_PORT}/test_scraper_app")

MYSQL_DB_ENGINE = 'InnoDB'
