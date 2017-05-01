import logging
import time

import newspaper
from feeder import nlp
from feeder.adapters import ArticleAdapter
from feeder.models import Article

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def import_articles(source):
    """Downloads, parses, transforms, and persists article data.

    :param source: Source - url and publisher of a source of articles
    """
    articles = Article.select(Article.url).filter(Article.publisher == source.publisher)
    source.build(ignore=[article.url for article in articles])
    for article in source.articles:
        persist(map_article(nlp.process(article)))

    # old
    # articles = retrieve_articles(source)
    # start = time.time()
    # for article in articles:
    #     article = nlp.process(parse(ArticleAdapter(article)))
    #     persist(map_article(article, source['publisher']))
    # parse_time = round(time.time() - start, 2)
    # log.info(f'Parsing and persisting time for {source["publisher"]} articles (secs): {parse_time}')


def parse(article):
    """Parses raw HTML into data attributes.

    :param article: ArticleAdapter - article object containing raw HTML
    :returns: ArticleAdapter - article object with parsed attributes
    """
    article.parse()
    return article


def map_article(parsed_data, publisher):
    """Converts parsed data into an acceptable format for the Article model.

    :param parsed_data: object - container of parsed data
    :returns: dict - article data
    """
    return {
        'publisher': publisher,
        'url': parsed_data.url,
        'authors': parsed_data.authors,
        'title': parsed_data.title,
        'date_published': parsed_data.publish_date,
        'keywords': parsed_data.keywords,
        'summary': parsed_data.summary,
    }


def persist(data):
    """Stuffs data into Article model and saves to database.

    :param data: dict - article data
    """
    Article.create(**data)
