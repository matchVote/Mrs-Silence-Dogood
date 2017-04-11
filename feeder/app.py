import logging
import time

import newspaper
from feeder.article import Article

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
sources = ['http://abcnews.com']

for source in sources:
    start = time.time()
    # .build caches article urls in ~/.newspaper_scraper/memoized
    paper = newspaper.build(source, memoize_articles=False)
    build_time = round(time.time() - start, 2)
    log.info(f'{paper.brand} article count: {paper.size()}; build time (secs): {build_time}')

    newspaper.news_pool.set([paper], threads_per_source=3)
    start = time.time()
    newspaper.news_pool.join()
    download_time = round(time.time() - start, 2)
    log.info(f'Download time for all articles (secs): {download_time}')

    for article in paper.articles:
        article.parse()
        Article.create(
            publisher=paper.brand,
            url=article.url,
            authors=article.authors,
            title=article.title,
            date_published=article.publish_date,)
