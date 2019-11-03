# -*- coding: utf-8 -*-

import argparse
import os
import sys
from pathlib import PurePath

import psycopg2
from decouple import AutoConfig

BASE_DIR = PurePath(os.path.abspath(__file__)).parent.parent
sys.path.insert(0, BASE_DIR)
env_folder = os.environ.get("RESUMEMAKR_ENV") or "dev"
config = AutoConfig(
    search_path=BASE_DIR.joinpath(
        "config/{env_folder}".format(env_folder=env_folder)
    )  # noqa
)


connection = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host=config("DJANGO_DATABASE_HOST"),
)  # noqa
connection.autocommit = True
cur = connection.cursor()

db_name = config("POSTGRES_DB")


def create_db():
    try:
        cur.execute(
            """
                CREATE DATABASE {name}
                OWNER {user} ENCODING 'utf-8'
            """.format(
                name=db_name, user=config("POSTGRES_USER")
            )
        )

        print('Database "{name}" successfully created.'.format(name=db_name))

    except psycopg2.errors.DuplicateDatabase:
        print('Database "{name}" already exists.'.format(name=db_name))


def drop_db():
    try:
        cur.execute(
            """
                DROP DATABASE {name}
            """.format(
                name=db_name
            )
        )

        print('Database "{name}" successfully dropped.'.format(name=db_name))
    except Exception:
        print('Database "{name}" can not be dropped.'.format(name=db_name))


parser = argparse.ArgumentParser(description="Set up and tear down database.")
group = parser.add_mutually_exclusive_group()

group.add_argument(
    "-c", "--create", action="store_true", help="creates the database"  # noqa
)


group.add_argument(
    "-d", "--drop", action="store_true", help="drops the database"  # noqa
)

args = parser.parse_args()

if args.create:
    create_db()
elif args.drop:
    drop_db()
else:
    parser.print_help()
