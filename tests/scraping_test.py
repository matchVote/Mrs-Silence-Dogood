import pytest

from dogood.scraping import scrape_source


@pytest.fixture
def source():
    return dict(url='', publisher='HeyThereNews')


class TestScraping:

    def test_scrape_source_returns_articles_for_all_urls_found(self, source):
        articles = scrape_source(source)
        assert len(articles) == 5
