import newspaper
import pytest
from dogood import source

TEST_CONFIG = {'url': 'http://test_brand.com', 'publisher': 'test_publisher'}


class TestSourceModuleFunctions:

    @pytest.fixture(autouse=True)
    def source(self):
        self.source = source.Source(TEST_CONFIG)
        self.source._source = MockNewspaperSource(
            urls=['http://art1.com', 'http://art2.com',
                  'http://ignore1.com', 'http://ignore2.com'])

    def test_download_articles_returns_objects_holding_article_html(self):
        articles = source.download_articles(
            self.source._source,
            TEST_CONFIG['publisher'])
        assert len(articles) == 4
        assert articles[0].url == 'http://art1.com'
        assert articles[0].html == 'Hey, I downloaded!'

    def test_remove_ignored_returns_a_subset_of_urls(self):
        all_urls = ['new.com', 'old2.com', 'old1.com']
        ignore = ['old1.com', 'old2.com']
        urls = source.remove_ignored(all_urls, ignore)
        assert urls == ['new.com']


class MockNewspaperSource:
    """Mock object to replace newspaper.Source."""

    def __init__(self, urls=None):
        self.articles = [newspaper.Article(url=url) for url in urls]

    def __len__(self):
        return len(self.articles)

    def download_articles(self):
        """Called by newspaper.news_pool.join() to download articles."""
        for article in self.articles:
            article.html = 'Hey, I downloaded!'

    def build(self):
        pass

    def size(self):
        return len(self)
