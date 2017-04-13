from collections import namedtuple
from datetime import datetime
import pytest

from feeder.article import Article
from feeder.consume import map_and_persist
from tests import use_transaction

ParsedArticle = namedtuple(
    'ParsedArticle',
    ['url', 'title', 'authors', 'publish_date', 'keywords', 'summary'])


class TestConsumption(object):
    """Test cases for consuming articles from sources."""

    def setup_method(self, _method):
        self.parsed_article = ParsedArticle(
            url='http://test_brand.com',
            title='Awesome article',
            authors=['Jim', 'Bob'],
            publish_date=datetime.now(),
            keywords=['tubular', 'radical', 'gnarley'],
            summary='One fine day...',)

    @use_transaction
    def test_map_and_persist_saves_articles_to_db(self):
        map_and_persist(self.parsed_article, 'test_publisher')
        assert len(Article.select()) == 1
