from multiprocessing import Pool
import os
import requests
from string import Template
import yaml

from feeder.consume import import_articles
from feeder.source import Source

with open('config/sources.yml') as f:
    config_template = Template(f.read())
    config_string = config_template.safe_substitute(os.environ)
    config = yaml.load(config_string)


def import_articles_from_apis():
    for api in config['apis']:
        adapter = APISourceAdapterFactory.create_adapter(config)
        APIImporter(adapter).import_articles()
    # newsapi = config['apis'][0]
    # sources_url = f'{newsapi["root_url"]}/{newsapi["version"]}/sources?language=en'
    # articles_params_template = f'?apiKey={newsapi["api_key"]}&source={{source_id}}'
    # base_url = f'{newsapi["root_url"]}/{newsapi["version"]}/articles'
    # response = requests.get(sources_url).json()
    # for source in response['sources']:
    #     params = articles_params_template.format(source_id=source['id'])
    #     articles_url = base_url + params
    #     articles_json = requests.get(articles_url).json()
    #     articles = articles_json['articles']
    #     print(f'{source["name"]} article count: {len(articles)}')
    #     for article in articles:
    #         print(f'Title: {article["title"]}')
    #         data = {newsapi['mapping'][key]: value for key, value in article.items()}
    #         data['publisher'] = source['name']
    #         Article.create(**data)


def scrape_articles_from_websites():
    sources = [Source(source) for source in config['sources']]
    with Pool(4) as pool:
        pool.map(import_articles, sources)
    print('\nFinished processing all sources.')


if __name__ == '__main__':
    import_articles_from_apis()
    # scrape_articles_from_websites()
