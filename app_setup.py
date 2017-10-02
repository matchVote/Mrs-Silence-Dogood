import os
import time

from peewee import OperationalError

from dogood import db, config
from dogood.models import Article, ArticleOfficial, Official

env = os.environ.get('FEEDER_ENV').upper()


def create_database():
    return 'createdb -h {host} -U {user} {database}'.format(**config)


def create_hstore_extension():
    cmd = 'psql -h {host} -U {user} {database} -c \'CREATE EXTENSION hstore;\''
    return cmd.format(**config)


if env in ['DEV', 'TEST']:
    print(f'Setting up {env} environment...')
    # Check if DB exists and create it if it doesn't
    try:
        db.connect()
    except OperationalError:
        print('No DB found. Creating...')
        time.sleep(5)  # wait for postgres to be running in container
        os.system(create_database())
        os.system(create_hstore_extension())
    # Create tables
    db.create_tables([Article, Official, ArticleOfficial], safe=True)

    # Load officials
    os.system('python -m data.load_dev_data')
