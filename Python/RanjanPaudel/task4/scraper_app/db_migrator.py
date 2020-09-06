import argparse

import db_models
import db_config

parser = argparse.ArgumentParser(description='MySQL migrator',
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--action",
                    help='To create/drop all tables',
                    choices=("create", "drop"),
                    required=True)


def main(arg_dict):
    if arg_dict['action'] == 'create':
        db_models.meta_data.create_all(db_config.engine)

        with db_models.conn.begin():
            inital_insert = db_models.tables['movie_list_meta'].insert().values([
                {"list_name": 'top_rated_movies'},
                {"list_name": 'top_rated_tv_shows'},
                {"list_name": 'most_popular_movies'},
                {"list_name": 'most_popular_tv_shows'}
            ])
            db_models.conn.execute(inital_insert)

    if arg_dict['action'] == 'drop':
        db_models.meta_data.drop_all(db_config.engine)


if __name__ == "__main__":
    opts = parser.parse_args()

    main(opts.__dict__)
