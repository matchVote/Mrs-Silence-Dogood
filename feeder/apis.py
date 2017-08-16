import requests

from feeder.models import Article


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
        Article.create(**article)

    def request_article_publishers(self):
        return requests.get(self.adapter.publishers_url).json()

    def request_articles(self, publisher):
        return requests.get(self.adapter.articles_url(publisher)).json()


def existing_article_urls():
    return [article.url for article in Article.select(Article.url)]


def is_new_article(article, publisher):
    return article['url'] not in existing_article_urls()


class NewsapiAdapter:
    '''Wrapper around Newsapi API configuration and JSON responses.'''

    def __init__(self, config):
        self.config = config
        self.publishers_url = self.construct_publishers_url()
        self.mapping = self.config['mapping']
        self.articles_json = None
        self._articles = []

    @property
    def articles(self):
        if not self._articles:
            self._articles = self.articles_json['articles']
        return self._articles

    def map(self, article):
        return {self.mapping[key]: value for key, value in article.items()}

    def publisher_list(self, publishers_json):
        return publishers_json['sources']

    def article_list(self, articles_json):
        return articles_json['articles']

    def construct_publishers_url(self):
        root_url = self.config['root_url']
        version = self.config['version']
        return f'{root_url}/{version}/sources?language=en'

    def articles_url(self, publisher):
        return self.base_url() + self.query_string(publisher)

    def base_url(self):
        return f'{self.config["root_url"]}/{self.config["version"]}/articles'

    def query_string(self, publisher):
        return f'?apiKey={self.config["api_key"]}&source={publisher["id"]}'


class APISourceAdapterFactory:
    '''Creates an adapter object based on API source specified in config.'''

    @classmethod
    def create_adapter(cls, config):
        if config['api_source'] == 'newsapi':
            return NewsapiAdapter(config)
