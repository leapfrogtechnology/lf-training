import sqlalchemy
from sqlalchemy.engine import Connection
from sqlalchemy import Table

import mysql_db.config as config
import mysql_db.models as mysql_models

tables = mysql_models.meta_data.tables
conn = Connection(config.engine)

if __name__ == "mysql_handler":
    def insert_many(table_name, dict_list):
        with conn.begin():
            conn.execute(
                tables[table_name].insert().values(dict_list))

    def fetch_all(table_name):
        result = []
        with conn.begin():
            out_put = conn.execute(
                tables[table_name].select())
            for row in out_put:
                result.append(dict(row))

        return result
