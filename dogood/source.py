import logging
import newspaper
from dogood import timer

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

    def build(self, ignore=None):
        """Scrapes source for article urls, removes the urls to ignore, and
        downloads the HTML for the remaining articles.

        :param ignore: list[str] - article urls not to download
        """
        self.build_source()
        if ignore:
            self.filter_out_ignored_articles(ignore)
        self.download_articles()

    def build_source(self):
        with timer(self.publisher, 'Building source...'):
            self._source.build()
        log.info(f'{self.publisher}: Total article count: {self._source.size()}')

    def filter_out_ignored_articles(self, urls_to_ignore):
        urls = [article.url for article in self._source.articles]
        filtered_urls = remove_ignored(urls, urls_to_ignore)[:ARTICLE_DOWNLOAD_LIMIT]
        self._source.articles = [newspaper.Article(url=url) for url in filtered_urls]

    def download_articles(self):
        self.articles = [ArticleAdapter(article, publisher=self.publisher)
                         for article in download_articles(self._source, self.publisher)]


def remove_ignored(urls, ignore):
    """Finds the difference between all source urls and existing urls.

    :param urls: list[str] - master url list
    :param ignore: list[str] - urls to ignore from master list
    :returns: list[str] - urls that aren't in ignore list
    """
    return list(set(urls) - set(ignore))


def download_articles(source, publisher):
    """Downloads HTML for all given urls.

    :param source: newspaper.Source - object containing urls to download
    :returns: list[newspaper.Article] - article objects containing HTML
    """
    with timer(publisher, f'Downloading {len(source.articles)} new articles...'):
        newspaper.news_pool.set([source], threads_per_source=MAX_DOWNLOAD_THREADS)
        newspaper.news_pool.join()
    return source.articles


class ArticleAdapter:
    """Wraps downloaded article data.
    This represents the boundary between external article data and the rest of
    the system, maintaining a standard interface for further processing.
    """

    def __init__(self, article, publisher=None):
        """This expects a newspaper.Article object.

        :param article: newspaper.Article - object containing downloaded article
        :param publisher: str - article's publisher
        """
        self.external_article = article
        self.publisher = publisher
        self.read_time = 0
        self.mentioned_officials = []

    def __getattr__(self, name):
        return getattr(self.external_article, name)
