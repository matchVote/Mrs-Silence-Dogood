import logging

from newspaper import Article, Source, news_pool

MAX_DOWNLOAD_THREADS = 5
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def scrape_source(config):
    log.info(f'Scraping source: {config["publisher"]}')
    source = create_source(config['url'])
    source.build()
    urls = [article.url for article in source.articles]
    log.info(f'Scraped {len(urls)} articles urls')
    return urls


def scrape_articles(urls):
    source = create_source()
    source.articles = [Article(url=url) for url in urls]
    articles = download_articles(source)
    return parse(articles)


def download_articles(source):
    news_pool.set([source], threads_per_source=MAX_DOWNLOAD_THREADS)
    news_pool.join()
    return source.articles


def parse(articles):
    for article in articles:
        article.parse()
    return articles


def create_source(url='http://'):
    return Source(url, memoize_articles=False, language='en')
