import logging

from peewee import IntegrityError

from dogood import utils
from dogood.models import Article, Official


log = logging.getLogger(__name__)


def insert(model):
    try:
        model.save()
    except IntegrityError as e:
        log.warning(f'IntegrityError skipped: {e}')


def article_urls_for_publisher(publisher):
    articles = Article.select(Article.url)
    publisher_articles = articles.filter(Article.publisher == publisher)
    return [article.url for article in publisher_articles]


def select_first_and_last_name_from_officials():
    return Official.select(Official.first_name, Official.last_name)


def map_to_model(article):
    model = Article()
    model.publisher = article.publisher
    model.url = article.url
    model.authors = article.authors
    model.title = article.title
    model.date_published = utils.normalize_date(article.publish_date)
    model.keywords = article.keywords
    model.summary = article.summary
    model.read_time = article.read_time
    model.mentioned_officials = article.mentioned_officials
    model.top_image_url = article.top_image
    model.source = article.publisher
    return model
