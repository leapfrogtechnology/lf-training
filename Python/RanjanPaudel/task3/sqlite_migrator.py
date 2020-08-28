import argparse

import sqlite_db.migrations as migrations

parser = argparse.ArgumentParser(description='SQLite migrator',
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--action",
                    help='To create/drop all tables',
                    choices=("create", "drop"),
                    required=True)


def main(arg_dict):
    if arg_dict['action'] == 'create':
        migrations.create_all()

    if arg_dict['action'] == 'drop':
        migrations.drop_all()


if __name__ == "__main__":
    opts = parser.parse_args()

    main(opts.__dict__)
