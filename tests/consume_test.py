from collections import namedtuple
from datetime import datetime, timedelta

import newspaper
import pytest
from pytest_mock import mocker

from dogood import consume
from dogood.source import ArticleAdapter, Source
from dogood.models import Article
from tests import transaction

TEST_DATE = datetime.now()
TEST_CONFIG = {'url': 'http://test_brand.com', 'publisher': 'test_publisher'}
EXPECTED_MAPPING = {
    'url': TEST_CONFIG['url'],
    'publisher': TEST_CONFIG['publisher'],
    'source': TEST_CONFIG['publisher'],
    'title': 'Awesome article',
    'authors': ['Jim', 'Bob'],
    'date_published': TEST_DATE,
    'keywords': ['tubular', 'radical', 'gnarley'],
    'summary': 'One fine day...',
    'read_time': 12,
    'mentioned_officials': ['Ricky Bobby', 'Davy Jones'],
    'top_image_url': 'http://image.com/hey'
    }


class MockSource:
    def __init__(self, config):
        self.publisher = config['publisher']
        self.articles = []

    def build(self, ignore=None):
        html = """<html><head><title>Awesome!</title></head>
        <body>Cool</body></html>"""
        articles = [
            newspaper.Article(url='http://art1.com'),
            newspaper.Article(url='http://art2.com')]
        for article in articles:
            article.html = html
            article.is_downloaded = article.is_parsed = True
            article.publish_date = TEST_DATE
        self.articles = [ArticleAdapter(article, publisher=self.publisher)
                         for article in articles]


def test_import_articles_downloads_processes_and_persists_articles(transaction):
    source = MockSource(TEST_CONFIG)
    source.build()
    consume.import_articles(source)
    result = Article.get(Article.url == 'http://art1.com')
    assert result.url == 'http://art1.com'
    assert result.title == 'Awesome!'
    assert result.read_time
    assert result.mentioned_officials == []


def test_parse_extracts_data_from_html():
    source = MockSource(TEST_CONFIG)
    source.build()
    # Parsing that test HTML ^ doesn't work properly with newspaper
    assert consume.parse(source.articles[0])


def test_map_article_converts_parsed_data_into_model_data():
    parsed_article = setup_parsed_article()
    mapping = consume.map_article(parsed_article)
    assert EXPECTED_MAPPING == mapping


def test_normalize_date_replaces_nulls_with_current_date():
    result = consume.normalize_date(None)
    assert result is not None


def test_normalize_date_replaces_future_dates_with_current_date():
    tomorrow = datetime.now() + timedelta(days=1)
    result = consume.normalize_date(tomorrow)
    assert result < tomorrow


def test_persist_saves_model_to_db(transaction):
    consume.persist(EXPECTED_MAPPING)
    articles = Article.select()
    assert len(articles) == 1
    assert articles[0].url == EXPECTED_MAPPING['url']
    assert articles[0].title == EXPECTED_MAPPING['title']


def setup_parsed_article():
    fields = ['url', 'title', 'keywords', 'summary', 'authors', 'publish_date',
              'read_time', 'mentioned_officials', 'publisher', 'top_image']
    ParsedArticle = namedtuple('ParsedArticle', fields)
    article = ParsedArticle(
        url='http://test_brand.com',
        title='Awesome article',
        keywords=['tubular', 'radical', 'gnarley'],
        summary='One fine day...',
        authors=['Jim', 'Bob'],
        publish_date=TEST_DATE,
        read_time=12,
        mentioned_officials=['Ricky Bobby', 'Davy Jones'],
        top_image='http://image.com/hey',
        publisher='test_publisher')
    return article
