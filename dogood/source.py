import logging

import newspaper

from dogood import timer
from dogood.adapters import ArticleAdapter

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

MAX_DOWNLOAD_THREADS = 3
ARTICLE_DOWNLOAD_LIMIT = 50


class Source:
    """Manages articles for a given publisher."""

    def __init__(self, config):
        self.url = config['url']
        self.publisher = config['publisher']
        self.articles = []
        self._source = newspaper.Source(config['url'], memoize_articles=False)

    def download_articles(self, ignore=None):
        self.scrape_source_for_all_article_urls()
        self.filter_articles(ignore)
        articles = download_articles(self._source, self.publisher)
        self.articles = [
            ArticleAdapter(article, publisher=self.publisher)
            for article in articles]

    def scrape_source_for_all_article_urls(self):
        with timer(self.publisher, 'Built source'):
            self._source.build()
        log.info(f'{self.publisher}: Total article count: {self._source.size()}')

    def filter_articles(self, urls_to_ignore):
        urls = [article.url for article in self._source.articles]
        if urls_to_ignore:
            urls = remove_ignored(urls, urls_to_ignore)
        filtered_urls = urls[:ARTICLE_DOWNLOAD_LIMIT]
        self._source.articles = [newspaper.Article(url=url) for url in filtered_urls]


def remove_ignored(urls, ignore):
    return list(set(urls) - set(ignore))


def download_articles(source, publisher):
    with timer(publisher, f'Downloaded {len(source.articles)} new articles'):
        newspaper.news_pool.set([source], threads_per_source=MAX_DOWNLOAD_THREADS)
        newspaper.news_pool.join()
    return source.articles
