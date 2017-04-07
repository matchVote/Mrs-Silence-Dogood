import logging
import os
import time
from peewee import OperationalError, ProgrammingError
from feeder import db, config
from feeder.article import Article

log = logging.getLogger(__name__)

# Check if DB exists and create it if it doesn't
try:
    db.connect()
except OperationalError:
    log.error('No DB found. Creating...')
    time.sleep(5)  # wait for postgres to be running in container
    os.system(f'createdb -h {config["host"]} -U {config["user"]} {config["database"]}')
    log.error('Done')

db.create_tables([Article], safe=True)
