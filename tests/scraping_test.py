import pytest

from dogood.scraping import scrape_articles, scrape_source


@pytest.fixture
def source():
    return dict(url='http://test_source:5000', publisher='HeyThereNews')


class TestScraping:

    def test_scrape_source_returns_list_of_urls_for_all_articles(self, source):
        urls = scrape_source(source)
        urls.sort()
        assert len(urls) == 5
        assert urls[0] == 'http://heytherenews.com/2017/10/01/an_article_about_clinton'

    def test_scrape_articles_downloads_and_parses_articles_from_given_urls(self):
        article = list(scrape_articles(['http://test_source:5000/article/1']))[0]
        assert 'Reid' in article.html
        assert article.title == 'Futureproofing your democracy'
