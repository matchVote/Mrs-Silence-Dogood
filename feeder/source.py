import logging
import newspaper
from feeder import timer

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class Source(object):
    """Manages articles for a given source publisher."""

    def __init__(self, config):
        """Constructor for Source."""
        self.url = config['url']
        self.publisher = config['publisher']
        self.articles = []
        self._source = newspaper.Source(config['url'], memoize_articles=False)

    def build(self, ignore=None):
        """Scrapes source for article urls, removes the urls to ignore, and
        downloads the HTML for the remaining articles.

        :param ignore: list - article urls not to download
        """
        with timer(self.publisher, 'Building source...'):
            self._source.build()
        log.info(f'{self.publisher}: Total article count: {self._source.size()}')

        urls = [article.url for article in self._source.articles]
        if ignore:
            urls = remove_ignored(urls, ignore)
        self._source.articles = [newspaper.Article(url=url) for url in urls]
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
        newspaper.news_pool.set([source], threads_per_source=3)
        newspaper.news_pool.join()
    return source.articles


class ArticleAdapter(object):
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
        """If attribute is not found on adapter, delegate to external article."""
        return getattr(self.external_article, name)
