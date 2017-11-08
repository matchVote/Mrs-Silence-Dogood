import logging

import newspaper

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
    articles = (newspaper.Article(url=url) for url in urls)
    articles = download_articles(articles)
    return parse(articles)


def download_articles(articles):
    for article in articles:
        article.download()
        yield article


def parse(articles):
    for article in articles:
        try:
            article.parse()
        except newspaper.article.ArticleException:
            pass
        else:
            yield article


def create_source(url='http://'):
    return newspaper.Source(url, memoize_articles=False, language='en')
