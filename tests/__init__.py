from feeder import db


def transaction(func):
    def test(*args):
        db.set_autocommit(False)
        db.begin()
        func(*args)
        db.rollback()
    return test
