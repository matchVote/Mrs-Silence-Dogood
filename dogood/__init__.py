from contextlib import contextmanager
import logging
import os
import time
import yaml

from playhouse.db_url import connect

logging.basicConfig(level=logging.INFO)
timer_log = logging.getLogger('Timer')

ENV = os.environ.get('FEEDER_ENV', 'dev')
db_url = os.environ.get('DATABASE_URL')

with open('config/database.yml') as f:
    config = yaml.load(f.read())[ENV]

if db_url is None:
    template = 'postgres://{user}:{password}@{host}:{port}/{database}'
    db_url = template.format(**config)
db = connect(db_url)


@contextmanager
def timer(publisher, message):
    """Shows how long some operation took for a specified publisher.

    :param publisher: str - source publisher
    :param message: str - operation specific message
    """
    start = time.time()
    yield
    duration = time.time() - start  # seconds
    duration_formatted = time.strftime('%H:%M:%S', time.gmtime(duration))
    timer_log.info(f'{publisher}: {message} -- duration {duration_formatted}')
