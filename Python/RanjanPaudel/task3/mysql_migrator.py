import argparse

import mysql_db.models as mysql_models
import mysql_db.config as mysql_config

parser = argparse.ArgumentParser(description='MySQL migrator',
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--action",
                    help='To create/drop all tables',
                    choices=("create", "drop"),
                    required=True)


def main(arg_dict):
    if arg_dict['action'] == 'create':
        mysql_models.meta_data.create_all(mysql_config.engine)

    if arg_dict['action'] == 'drop':
        mysql_models.meta_data.drop_all(mysql_config.engine)


if __name__ == "__main__":
    opts = parser.parse_args()

    main(opts.__dict__)
