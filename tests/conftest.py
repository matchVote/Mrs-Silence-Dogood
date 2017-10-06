import pytest

from dogood.models import BaseModel


@pytest.fixture
def transaction():
    """Wraps test function in database transaction."""
    db = BaseModel._meta.database
    db.set_autocommit(False)
    db.begin()
    try:
        yield
    except Exception as e:
        raise Exception('Failure in transaction') from e
    finally:
        db.rollback()
