# What good shall I do this day?

from datetime import datetime
import logging

from peewee import IntegrityError
import requests

from dogood import nlp, timer
from dogood.models import Article

log = logging.getLogger(__name__)


class APIImporter:
    '''Requests, maps, and writes articles from API to database.'''

    def __init__(self, adapter):
        self.adapter = adapter

    def import_articles(self):
        for publisher, article in self.download_articles():
            article = self.adapter.map(article)
            self.persist_article(article, publisher)

    def download_articles(self):
        response = self.request_article_publishers()
        for publisher in self.adapter.publisher_list(response):
            response = self.request_articles(publisher)
            for article in self.adapter.article_list(response):
                if is_new_article(article, publisher):
                    yield publisher, article

    def persist_article(self, article, publisher):
        article['publisher'] = publisher['name']
        article['source'] = self.adapter.source
        Article.create(**article)

    def request_article_publishers(self):
        return requests.get(self.adapter.publishers_url).json()

    def request_articles(self, publisher):
        return requests.get(self.adapter.articles_url(publisher)).json()


def is_new_article(article, publisher):
    return article['url'] not in existing_article_urls()


def existing_article_urls():
    return [article.url for article in Article.select(Article.url)]


def import_articles(source):
    """Downloads, parses, transforms, and persists article data.

    :param source: Source - url and publisher of a source of articles
    """
    source.build(ignore=existing_article_urls_by_publisher(source.publisher))
    with timer(source.publisher, 'Processing articles...'):
        for article in source.articles:
            persist(map_article(nlp.process(parse(article))))


def existing_article_urls_by_publisher(publisher):
    """Returns URLs for previously imported articles for publisher.

    :param publisher: str - article publisher
    :returns: list[str] - urls for existing articles
    """
    articles = Article.select(Article.url)
    publisher_articles = articles.filter(Article.publisher == publisher)
    return [article.url for article in publisher_articles]


def parse(article):
    """Parses raw HTML into data attributes.

    :param article: ArticleAdapter - article object containing raw HTML
    :returns: ArticleAdapter - article object with parsed attributes
    """
    try:
        article.parse()
    except ValueError as error:
        log.warn(f'{article.pubisher}: Parsing error: {error}')
    return article


def map_article(article):
    """Converts parsed data into an acceptable format for the Article model.

    :param article: object - container of parsed data
    :returns: dict - article data
    """
    return {
        'publisher': article.publisher,
        'url': article.url,
        'authors': article.authors,
        'title': article.title,
        'date_published': normalize_date(article.publish_date),
        'keywords': article.keywords,
        'summary': article.summary,
        'read_time': article.read_time,
        'mentioned_officials': article.mentioned_officials,
        'top_image_url': article.top_image,
        'source': article.publisher
        }


def normalize_date(date):
    if date:
        current_date = datetime.now()
        if date > current_date:
            date = current_date
    else:
        date = datetime.now()
    return date


def persist(data):
    """Stuffs data into Article model and saves to database.

    :param data: dict - article data
    """
    try:
        Article.create(**data)
    except IntegrityError as e:
        log.warn(f'IntegrityError skipped: {e}')
