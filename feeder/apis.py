from feeder.models import Article


class APIImporter:

    def __init__(self, adapter):
        self.adapter = adapter

    def import_articles(self):
        self.download_articles()
        self.persist_articles()

    def download_articles(self):
        for source in self.request_sources():
            self.adapter.articles_json = self.request_articles(source)

    def persist_articles(self):
        for article in self.adapter.articles:
            print(f'Title: {article["title"]}')
            data = {newsapi['mapping'][key]: value for key, value in article.items()}
            data['publisher'] = source['name']
            Article.create(**data)

    def request_sources(self):
        return requests.get(self.adapter.sources_url).json()

    def request_articles(self, source):
        return requests.get(self.adapter.articles_url).json()


class NewsapiAdapter:
    '''Wrapper around Newsapi API responses.'''

    def __init__(self, config):
        self.config = config
        self.sources_url = self.construct_sources_url()
        self.articles_url = self.construct_articles_url()
        self.articles_json = None
        self.articles = []

    @property
    def articles(self):
        if not self.articles:
            self.articles = self.articles_json['articles']
        return self.articles

    def construct_sources_url(self):
        root_url = self.config['root_url']
        version = self.config['version']
        return f'{root_url}/{version}/sources?language=en'

    def construct_articles_url(self):
        articles_params_template = f'?apiKey={newsapi["api_key"]}&source={{source_id}}'
        base_url = f'{newsapi["root_url"]}/{newsapi["version"]}/articles'
        params = articles_params_template.format(source_id=source['id'])
        articles_url = base_url + params


class APISourceAdapterFactory:
    '''Creates an adapter object based on API source specified in config.'''

	@classmethod
	def create_adapter(cls, config):
        if config['api_source'] == 'newsapi':
            return NewsapiAdapter(config)

