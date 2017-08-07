import pytest
from feeder import construct_db_url


class TestFeeder:
    """Test cases for behavior in Feeder.__init__."""

    @pytest.fixture(autouse=True)
    def config(self):
        self.config = {
            'user': 'bob',
            'password': '12345',
            'host': 'localhost',
            'port': '9876',
            'database': 'pachuko'
            }

    def test_construct_db_url_returns_full_url_from_config(self):
        url = construct_db_url(self.config)
        assert 'postgres://bob:12345@localhost:9876/pachuko' == url
