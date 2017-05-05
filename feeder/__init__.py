from contextlib import contextmanager
import logging
import os
import time
import yaml

from playhouse.postgres_ext import PostgresqlExtDatabase

logging.basicConfig(level=logging.INFO)
timer_log = logging.getLogger('Timer')

env = os.environ.get('FEEDER_ENV', 'dev')
with open('config/database.yml') as f:
    config = yaml.load(f.read())[env]

db = PostgresqlExtDatabase(
    config['database'],
    user=config['user'],
    password=config['password'],
    host=config['host'],
    port=config['port'])


@contextmanager
def timer(message):
    start = time.time()
    timer_log.info(message)
    yield
    duration = round(time.time() - start, 2)
    timer_log.info(f'Duration: {duration} secs')
