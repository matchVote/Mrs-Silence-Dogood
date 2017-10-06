import os

from playhouse.postgres_ext import PostgresqlExtDatabase
import yaml


class Database:
    """Decorator for peewee database object."""

    def __init__(self):
        self.config = load_config()
        self.db = setup_database(self.config)

    def __getattr__(self, attribute):
        return getattr(self.db, attribute)

    def create_database(self):
        command = 'createdb -h {host} -U {user} {database}'
        os.system(command.format(**self.config))

    def create_hstore_extension(self):
        cmd = "psql -h {host} -U {user} {database} -c 'CREATE EXTENSION hstore;'"
        os.system(cmd.format(**self.config))


def load_config():
    env = os.getenv('FEEDER_ENV')
    with open('config/database.yml') as f:
        return yaml.load(f.read())[env]


def setup_database(config):
    return PostgresqlExtDatabase(**config)
