from contextlib import contextmanager
import logging
import os
import time
import yaml

from playhouse.db_url import connect

logging.basicConfig(level=logging.INFO)
timer_log = logging.getLogger('Timer')

env = os.environ.get('FEEDER_ENV', 'dev')
db_url = os.environ.get('DATABASE_URL')

with open('config/database.yml') as f:
    config = yaml.load(f.read())[env]


def construct_db_url(config):
    template = 'postgres://{user}:{password}@{host}:{port}/{database}'
    return template.format(**config)


db = connect(db_url or construct_db_url(config))


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
    timer_log.info(f'{publisher}: {message} -- duration {duration_formatted}')
