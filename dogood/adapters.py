class ArticleAdapter:
    """Wraps downloaded article data.
    This represents the boundary between external article data and the rest of
    the system, maintaining a standard interface for further processing.
    """

    def __init__(self, article, publisher=None):
        self.external_article = article
        self.publisher = publisher
        self.read_time = 0
        self.mentioned_officials = []

    def __getattr__(self, name):
        return getattr(self.external_article, name)


class APISourceAdapterFactory:
    '''Creates an adapter object based on API source specified in config.'''

    @classmethod
    def create_adapter(cls, config):
        if config['api_source'] == 'newsapi':
            return NewsapiAdapter(config)


class NewsapiAdapter:
    '''Wrapper around Newsapi API configuration and JSON responses.'''

    def __init__(self, config):
        self.config = config
        self.publishers_url = self.construct_publishers_url()
        self.mapping = self.config['mapping']
        self.source = self.config['api_source']
        self.articles_json = None
        self._articles = []

    @property
    def articles(self):
        if not self._articles:
            self._articles = self.articles_json['articles']
        return self._articles

    def map(self, article):
        data = {self.mapping[key]: value for key, value in article.items()}
        data = convert_authors_to_list(data)
        return data

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


def convert_authors_to_list(data):
    author = data['authors']
    data['authors'] = [author] if author else []
    return data
