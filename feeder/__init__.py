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
def timer(publisher, message):
    """Shows how long some operation took for a specified publisher.

    :param publisher: str - source publisher
    :param message: str - operation specific message
    """
    start = time.time()
    timer_log.info(f'{publisher}: {message}')
    yield
    duration = time.time() - start  # seconds
    duration_formatted = time.strftime('%H:%M:%S', time.gmtime(duration))
    timer_log.info(f'{publisher}: duration {duration_formatted}')
