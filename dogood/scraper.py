import logging

from dogood import repo, timer
from dogood.nlp import NLProcessor

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class Scraper:
    """Downloads, parses, and processes articles from a given source."""

    def __init__(self, source):
        self.source = source
        self.parsed_articles = []
        self._political_articles = []

    def execute(self):
        self.download_and_parse_new_articles()
        count = len(self.political_articles)
        with timer(self.source.publisher, f'{count} political articles processed'):
            for article in self.political_articles:
                self.process_article(article)

    def existing_articles(self):
        return repo.article_urls_for_publisher(self.source.publisher)

    def download_and_parse_new_articles(self):
        self.source.download_articles(ignore=self.existing_articles())
        self.parsed_articles = [parse(article) for article in self.source.articles]

    @property
    def political_articles(self):
        if not self._political_articles:
            self._political_articles = [
                article
                for article in self.parsed_articles
                if is_political(article)]
        return self._political_articles

    def process_article(self, article):
        nlp = NLProcessor(article)
        nlp.process_article()
        self.persist_article(nlp.article)

    def persist_article(self, article):
        repo.insert(repo.map_to_model(article))


def parse(article):
    try:
        article.parse()
    except ValueError as error:
        log.warn(f'{article.pubisher}: Parsing error: {error}')
    return article


def is_political(article):
    nlp = NLProcessor(article)
    classification = nlp.classify_article()
    if classification == 'politics':
        return True
    return False
