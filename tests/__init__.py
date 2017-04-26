from feeder import db


def use_transaction(func):
    def test(*args):
        db.set_autocommit(False)
        db.begin()
        try:
            func(*args)
        except Exception as e:
            raise Exception('Failure in transaction') from e
        finally:
            db.rollback()
    return test


class SourceArticle(object):
    """Mock article created by source object."""

    def __init__(self, url=None):
        self.url = url
