from collections import namedtuple
from datetime import datetime

import newspaper
import pytest
from pytest_mock import mocker

from feeder import consume
from feeder.models import Article
from feeder.adapters import ArticleAdapter, SourceAdapter
from tests import transaction

test_date = datetime.now()
test_config = {'url': 'http://test_brand.com', 'publisher': 'test_publisher'}
expected_mapping = {
    'url': test_config['url'],
    'publisher': test_config['publisher'],
    'title': 'Awesome article',
    'authors': ['Jim', 'Bob'],
    'date_published': test_date,
    'keywords': ['tubular', 'radical', 'gnarley'],
    'summary': 'One fine day...',
}


@pytest.fixture
def source():
    source = SourceAdapter(test_config)
    source.articles = [
        newspaper.Article(url='http://art1.com'),
        newspaper.Article(url='http://art2.com')]
    return source


def test_import_articles_downloads_processes_and_persists_articles(transaction, mocker, source):
    mocker.patch('newspaper.build')
    newspaper.build.return_value = source
    mocker.patch('newspaper.news_pool', new=MockNewsPool(source))

    consume.import_articles(test_config)  # this source doesn't matter
    result = Article.get(Article.url == 'http://nowhere.com')
    assert result.title == 'Awesome!'


def test_collect_article_urls_sets_articles_on_source(source):
    # mocker.patch('newspaper.build')
    # newspaper.build.return_value = source
    consume.collect_article_urls(source)
    assert source.articles == ['http://art1.com', 'http://art2.com']


def test_extract_new_urls_returns_urls_that_havent_been_consumed_before():
    all_urls = ['new.com', 'old2.com', 'old1.com']
    existing_urls = ['old1.com', 'old2.com']
    urls = consume.extract_new_urls(all_urls, existing_urls)
    assert urls == ['new.com']


def test_existing_articles_returns_a_list_of_previously_consumed_urls(transaction):
    Article.create(**expected_mapping)
    urls = consume.existing_articles(test_config)
    assert urls == ['http://test_brand.com']


def test_download_articles_returns_objects_holding_article_html(mocker):
    mocker.patch('newspaper.news_pool', new=MockNewsPool())
    articles = consume.download_articles(['http://art1.com', 'http://art2.com'])
    assert articles[0].html == "It's dope!"
    assert articles[0].url == 'http://art1.com'


def test_retrieve_articles_returns_article_objects_downloaded_from_a_source(mocker, source):
    mocker.patch('newspaper.build')
    newspaper.build.return_value = source
    mocker.patch('newspaper.news_pool')
    articles = consume.retrieve_articles(test_config)
    assert len(articles) == 2


def test_parse_extracts_data_from_html():
    external_article = newspaper.Article(url='test.com')
    external_article.is_downloaded = True
    article = ArticleAdapter(external_article)
    assert consume.parse(article)


def test_map_article_converts_parsed_data_into_model_data():
    parsed_article = setup_parsed_article()
    mapping = consume.map_article(parsed_article, 'test_publisher')
    assert mapping == expected_mapping


def test_persist_saves_model_to_db(transaction):
    consume.persist(expected_mapping)
    articles = Article.select()
    assert len(articles) == 1
    assert articles[0].url == expected_mapping['url']


def setup_parsed_article():
    article = newspaper.Article(
        url='http://test_brand.com',
        title='Awesome article')
    article.keywords = ['tubular', 'radical', 'gnarley']
    article.summary = 'One fine day...'
    article.authors = ['Jim', 'Bob']
    article.publish_date = test_date
    return article


class MockNewsPool(object):
    """Mock object to control article downloading."""

    def __init__(self, source=None):
        self.source = source

    def set(self, sources, threads_per_source=None):
        if self.source is None:
            self.source = sources[0]

    def join(self):
        for article in self.source.articles:
            article.is_downloaded = True
            article.html = "It's dope!"
