import newspaper
import pytest
from feeder import source

TEST_CONFIG = {'url': 'http://test_brand.com', 'publisher': 'test_publisher'}


class TestSource(object):
    """Test cases for Source class."""

    @pytest.fixture(autouse=True)
    def source(self):
        self.source = source.Source(TEST_CONFIG)
        self.source._source = MockNewspaperSource(
            urls=['http://art1.com', 'http://art2.com',
                  'http://ignore1.com', 'http://ignore2.com'])

    def test_build_extracts_and_downloads_articles_from_source(self):
        self.source.build()
        assert len(self.source.articles) == 4

    def test_build_ignores_given_urls(self):
        self.source.build(ignore=['http://ignore1.com', 'http://ignore2.com'])
        assert len(self.source.articles) == 2

    def test_download_articles_returns_objects_holding_article_html(self):
        articles = source.download_articles(self.source._source)
        assert len(articles) == 4
        assert articles[0].url == 'http://art1.com'
        assert articles[0].html == 'Hey, I downloaded!'

    def test_remove_ignored_returns_a_subset_of_urls(self):
        all_urls = ['new.com', 'old2.com', 'old1.com']
        ignore = ['old1.com', 'old2.com']
        urls = source.remove_ignored(all_urls, ignore)
        assert urls == ['new.com']


class MockNewspaperSource(object):
    """Mock object to replace newspaper.Source."""

    def __init__(self, urls=None):
        self.articles = [newspaper.Article(url=url) for url in urls]

    def download_articles(self):
        """Called by newspaper.news_pool.join() to download articles."""
        for article in self.articles:
            article.html = 'Hey, I downloaded!'

    def build(self):
        pass

    def size(self):
        return len(self)

    def __len__(self):
        return len(self.articles)
