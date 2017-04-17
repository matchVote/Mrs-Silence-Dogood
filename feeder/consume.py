import logging
import time

import newspaper
from feeder.article import Article

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def import_articles(source):
    """Downloads, parses, transforms, and persists article data.

    :param source: dict - url and publisher of a source of articles
    """
    articles = retrieve_articles(source)
    start = time.time()
    for article in articles:
        article.parse()
        article.nlp()
        persist(map_article(article, source['publisher']))
    parse_time = round(time.time() - start, 2)
    log.info(f'Parsing and persisting time for {source["publisher"]} articles (secs): {parse_time}')


def retrieve_articles(source):
    """Collects articles urls from source, diffs them against previously imported
    articles, and downloads new article data.

    :param source: dict - url and publisher of a source of articles
    :returns: list[newspaper.Article] - list of parsed data in article objects
    """
    # all_urls = collect_article_urls(source)
    # urls = extract_new_urls(all_urls, existing_articles(source))
    # return download_articles(urls)


    log.info(f'Building source: {source["publisher"]}')
    start = time.time()
    # newspaper.build caches article urls in ~/.newspaper_scraper/memoized
    paper = newspaper.build(source['url'], memoize_articles=False)
    build_time = round(time.time() - start, 2)
    log.info(f'{source["publisher"]} article count: {paper.size()}; build time (secs): {build_time}')

    newspaper.news_pool.set([paper], threads_per_source=3)
    start = time.time()
    newspaper.news_pool.join()
    download_time = round(time.time() - start, 2)
    log.info(f'Download time for {source["publisher"]} articles (secs): {download_time}')

    return paper.articles


def collect_article_urls(source):
    log.info(f'Building source: {source["publisher"]}')
    start = time.time()
    # newspaper.build caches article urls in ~/.newspaper_scraper/memoized
    paper = newspaper.build(source['url'], memoize_articles=False)
    build_time = round(time.time() - start, 2)
    log.info(f'{source["publisher"]} article count: {paper.size()}; build time (secs): {build_time}')
    return [article.url for article in paper.articles]


def extract_new_urls(all_urls, old_urls):
    return list(set(all_urls) - set(old_urls))


def existing_articles(source):
    """TODO

    :param source: dict - url and publisher of a source of articles
    :returns: list - article urls that have already been imported
    """
    articles = Article.select().filter(Article.publisher == source['publisher'])
    return [article.url for article in articles]


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
