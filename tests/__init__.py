from feeder import db


def use_transaction(func):
    def test(*args):
        db.set_autocommit(False)
        db.begin()
        func(*args)
        db.rollback()
    return test
