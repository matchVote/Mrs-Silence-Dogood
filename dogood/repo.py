from datetime import datetime
import logging

from peewee import IntegrityError

from dogood import utils
from dogood.models import Article, ArticleOfficial, Official


log = logging.getLogger(__name__)


def insert(model):
    try:
        model.save()
    except IntegrityError as e:
        log.warning(f'IntegrityError skipped: {e}')
        log.warning(f'Failed save -- publisher: {model.publisher}; time: {datetime.now()}')


def article_urls():
    return [article.url for article in Article.select(Article.url)]


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


def link_articles_to_officials(article):
    ids = {'article_id': article.id}
    for official in article.mentioned_officials:
        ids['official_id'] = official.id
        ArticleOfficial.create(**ids)


def official_ids_by_first_and_last_names(first_names, last_names):
    return Official.select(Official.id).where(
        Official.first_name << first_names,
        Official.last_name << last_names)
