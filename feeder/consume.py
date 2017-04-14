import logging
import time

import newspaper
from feeder.article import Article

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def import_articles(source):
    """Downloads, parses, transforms, and persists article data.

    :param source: dict - url and label of a source of articles
    """
    articles = download_articles(source)
    start = time.time()
    for article in paper.articles:
        article.parse()
        article.nlp()
        persist(map_article(article, source['label']))
    parse_time = round(time.time() - start, 2)
    log.info(f'Parsing and persisting time for {source["label"]} articles (secs): {parse_time}')


def download_articles(source):
    """Collects articles urls from source, diffs them against previously imported
    articles, and downloads new article data.

    :param source: dict - url and label of a source of articles
    :returns: list[newspaper.Article] - list of parsed data in article objects
    """
    log.info(f'Building source: {source["label"]}')
    start = time.time()
    # newspaper.build caches article urls in ~/.newspaper_scraper/memoized
    paper = newspaper.build(source['url'], memoize_articles=False)
    build_time = round(time.time() - start, 2)
    log.info(f'{source["label"]} article count: {paper.size()}; build time (secs): {build_time}')

    # Add article url diff

    newspaper.news_pool.set([paper], threads_per_source=3)
    start = time.time()
    newspaper.news_pool.join()
    download_time = round(time.time() - start, 2)
    log.info(f'Download time for {source["label"]} articles (secs): {download_time}')

    return paper.articles


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
