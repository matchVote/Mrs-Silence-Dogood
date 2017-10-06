from contextlib import contextmanager
from datetime import datetime, timezone
import logging
import time

logging.basicConfig(level=logging.INFO)
timer_log = logging.getLogger('Timer')


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


def normalize_date(date):
    if date:
        current_date = datetime.now(timezone.utc)
        date = date.replace(tzinfo=timezone.utc)
        if date > current_date:
            date = current_date
    else:
        date = datetime.now(timezone.utc)
    return date
