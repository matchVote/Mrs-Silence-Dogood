import logging
import time
import yaml

import newspaper
from feeder.article import Article

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
with open('config/sources.yml') as f:
    sources = yaml.load(f)['sources']


def import_articles(source):
    log.info(f'Building source: {source}')
    start = time.time()
    # newspaper.build caches article urls in ~/.newspaper_scraper/memoized
    paper = newspaper.build(source, memoize_articles=False)
    build_time = round(time.time() - start, 2)
    log.info(f'{paper.brand.upper()} article count: {paper.size()}; build time (secs): {build_time}')

    newspaper.news_pool.set([paper], threads_per_source=3)
    start = time.time()
    newspaper.news_pool.join()
    download_time = round(time.time() - start, 2)
    log.info(f'Download time for {paper.brand.upper()} articles (secs): {download_time}')

    start = time.time()
    for article in paper.articles:
        article.parse()
        article.nlp()
        Article.create(
            publisher=paper.brand,
            url=article.url,
            authors=article.authors,
            title=article.title,
            date_published=article.publish_date,
            keywords=article.keywords,
            summary=article.summary,)
    parse_time = round(time.time() - start, 2)
    log.info(f'Parsing and persisting time for {paper.brand.upper()} articles (secs): {parse_time}')


if __name__ == '__main__':
    for source in sources:
        import_articles(f'http://{source}')

