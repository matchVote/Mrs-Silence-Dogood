import os
import time

from peewee import OperationalError

from dogood import Database
from dogood.models import Article, ArticleOfficial, Official

env = os.environ.get('FEEDER_ENV')
db = Database()


if env in ['dev', 'test']:
    print(f'Setting up {env.upper()} environment...')
    # Check if DB exists and create it if it doesn't
    try:
        db.connect()
    except OperationalError:
        print('No DB found. Creating...')
        time.sleep(5)  # wait for postgres to be running in container
        db.create_database()
        db.create_hstore_extension()
    # Create tables
    db.create_tables([Article, Official, ArticleOfficial], safe=True)

    # Load officials
    os.system('python -m data.load_dev_data')
