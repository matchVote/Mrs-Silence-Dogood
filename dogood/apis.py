import requests

from dogood.models import Article  # TODO: use repo instead


class APIImporter:
    '''Requests, maps, and writes articles from API to database.'''

    def __init__(self, adapter):
        self.adapter = adapter

    def import_articles(self):
        for publisher, article in self.download_articles():
            article = self.adapter.map(article)
            self.persist_article(article, publisher)

    def download_articles(self):
        response = self.request_article_publishers()
        for publisher in self.adapter.publisher_list(response):
            response = self.request_articles(publisher)
            for article in self.adapter.article_list(response):
                if is_new_article(article, publisher):
                    yield publisher, article

    def persist_article(self, article, publisher):
        article['publisher'] = publisher['name']
        article['source'] = self.adapter.source
        Article.create(**article)

    def request_article_publishers(self):
        return requests.get(self.adapter.publishers_url).json()

    def request_articles(self, publisher):
        return requests.get(self.adapter.articles_url(publisher)).json()


def is_new_article(article, publisher):
    return article['url'] not in existing_article_urls()


def existing_article_urls():
    return [article.url for article in Article.select(Article.url)]
