import logging

from newspaper import Article, Source, news_pool

MAX_DOWNLOAD_THREADS = 5
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def scrape_source(config):
    source = create_source(config['url'])
    source.build()
    return [article.url for article in source.articles]


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


# class Scraper:
#     """Downloads, parses, and processes articles from a given source."""
#
#     def __init__(self, source):
#         self.source = source
#         self.parsed_articles = []
#         self._political_articles = []
#
#     @property
#     def political_articles(self):
#         if not self._political_articles:
#             for article in self.parsed_articles:
#                 if ArticleClassifier(article).is_political:
#                     self._political_articles.append(article)
#         return self._political_articles
#
#     def execute(self):
#         self.download_and_parse_new_articles()
#         message = f'{len(self.political_articles)} political articles processed'
#         with timer(self.source.publisher, message):
#             for article in self.political_articles:
#                 self.process_article(article)
#
#     def download_and_parse_new_articles(self):
#         self.source.download_articles(ignore=self.existing_articles())
#         self.parsed_articles = [parse(article) for article in self.source.articles]
#
#     def existing_articles(self):
#         return repo.article_urls()
#
#     def process_article(self, article):
#         nlp = NLProcessor(article)
#         nlp.process_article()
#         article = self.persist_article(nlp.article)
#         repo.link_articles_to_officials(article)
#
#     def persist_article(self, article):
#         article = repo.map_to_model(article)
#         repo.insert(article)
#         return article
#
#
# def parse(article):
#     try:
#         article.parse()
#     except ValueError as error:
#         log.warn(f'{article.pubisher}: Parsing error: {error}')
#     return article
