import logging
import os
import time
from peewee import OperationalError, ProgrammingError
from feeder import db, config
from feeder.models import Article

env = os.environ.get('FEEDER_ENV').upper()

print('Setting up {} environment...'.format(env))
# Check if DB exists and create it if it doesn't
try:
    db.connect()
except OperationalError:
    print('No DB found. Creating...')
    time.sleep(5)  # wait for postgres to be running in container
    os.system(f'createdb -h {config["host"]} -U {config["user"]} {config["database"]}')
    os.system(f'psql -h {config["host"]} -U {config["user"]} {config["database"]} -c \'CREATE EXTENSION hstore;\'')

# Create tables
db.create_tables([Article], safe=True)

print('Done...party on!')
