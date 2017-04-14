from collections import namedtuple
from datetime import datetime
import pytest

from feeder.article import Article
from feeder.consume import map_article, persist

ParsedArticle = namedtuple(
    'ParsedArticle',
    ['url', 'title', 'authors', 'publish_date', 'keywords', 'summary'])

test_date = datetime.now()
expected_mapping = {
    'url': 'http://test_brand.com',
    'publisher': 'test_publisher',
    'title': 'Awesome article',
    'authors': ['Jim', 'Bob'],
    'date_published': test_date,
    'keywords': ['tubular', 'radical', 'gnarley'],
    'summary': 'One fine day...',
}


class TestConsumption(object):
    """Test cases for consuming articles from sources."""

    def setup_method(self, _method):
        self.parsed_article = ParsedArticle(
            url='http://test_brand.com',
            title='Awesome article',
            authors=['Jim', 'Bob'],
            publish_date=test_date,
            keywords=['tubular', 'radical', 'gnarley'],
            summary='One fine day...',)

    def test_map_article_converts_parsed_data_into_model_data(self):
        mapping = map_article(self.parsed_article, 'test_publisher')
        assert mapping == expected_mapping

    def test_persist_saves_model_to_db(self):
        persist(expected_mapping)
        articles = Article.select()
        assert len(articles) == 1
        assert articles[0].url == expected_mapping['url']
