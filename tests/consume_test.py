from collections import namedtuple
from datetime import datetime

import newspaper
import pytest
from pytest_mock import mocker

from feeder.article import Article
import feeder.consume
from tests import use_transaction

ParsedArticle = namedtuple(
    'ParsedArticle',
    ['url', 'title', 'authors', 'publish_date', 'keywords', 'summary'])

test_date = datetime.now()
test_source = {'url': 'http://test_brand.com', 'publisher': 'test_publisher'}
expected_mapping = {
    'url': test_source['url'],
    'publisher': test_source['publisher'],
    'title': 'Awesome article',
    'authors': ['Jim', 'Bob'],
    'date_published': test_date,
    'keywords': ['tubular', 'radical', 'gnarley'],
    'summary': 'One fine day...',
}


class TestConsume(object):
    """Test cases for consuming articles from sources."""

    def setup_method(self, _method):
        self.mock_source = MockSource(articles=[
            SourceArticle(url='art1.com'),
            SourceArticle(url='art2.com')
        ])
        self.parsed_article = ParsedArticle(
            url='http://test_brand.com',
            title='Awesome article',
            authors=['Jim', 'Bob'],
            publish_date=test_date,
            keywords=['tubular', 'radical', 'gnarley'],
            summary='One fine day...',)

    def test_collect_article_urls_returns_all_article_urls_for_source(self, mocker):
        mocker.patch.object(newspaper, 'build')
        newspaper.build.return_value = self.mock_source
        urls = feeder.consume.collect_article_urls(test_source)
        assert urls == ['art1.com', 'art2.com']

    def test_extract_new_urls_returns_urls_that_havent_been_consumed_before(self):
        all_urls = ['new.com', 'old2.com', 'old1.com']
        existing_urls = ['old1.com', 'old2.com']
        urls = feeder.consume.extract_new_urls(all_urls, existing_urls)
        assert urls == ['new.com']

    @use_transaction
    def test_existing_articles_returns_a_list_of_previously_consumed_urls(self):
        Article.create(**expected_mapping)
        urls = feeder.consume.existing_articles(test_source)
        assert urls == ['http://test_brand.com']

    def test_download_articles_returns_objects_holding_article_html(self, mocker):
        mocker.patch.object(newspaper, 'news_pool')
        articles = feeder.consume.download_articles(['art1.com', 'art2.com'])
        assert articles[0].html == ''

    def test_retrieve_articles_returns_article_objects_downloaded_from_a_source(self, mocker):
        # Article.create(url='test-url', publisher=test_source['publisher'])
        mocker.patch.object(newspaper, 'build')
        mocker.patch.object(newspaper, 'news_pool')
        newspaper.build.return_value = self.mock_source
        articles = feeder.consume.retrieve_articles(test_source)
        assert len(articles) == 2

    def test_map_article_converts_parsed_data_into_model_data(self):
        mapping = feeder.consume.map_article(self.parsed_article, 'test_publisher')
        assert mapping == expected_mapping

    @use_transaction
    def test_persist_saves_model_to_db(self):
        feeder.consume.persist(expected_mapping)
        articles = Article.select()
        assert len(articles) == 1
        assert articles[0].url == expected_mapping['url']


class MockSource(object):
    """Mock object to use in place of a source."""

    def __init__(self, articles):
        self.articles = articles

    def size(self):
        return len(self.articles)

    def download_articles(self):
        """Used by newspaper.news_pool"""
        return []


class SourceArticle(object):
    """Mock article created by source object."""

    def __init__(self, url):
        self.url = url
