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


def import_articles_from_api():
    """TODO: Docstring for import_articles_from_api."""
    newsapi = config['apis'][0]
    sources_url = f'{newsapi["root_url"]}/{newsapi["version"]}/sources?language=en'
    articles_params_template = f'?apiKey={newsapi["api_key"]}&source={{source_id}}'
    articles_url = f'{newsapi["root_url"]}/{newsapi["version"]}/articles'

    response = requests.get(sources_url).json()
    source = response['sources'][1]
    params = articles_params_template.format(source_id=source['id'])
    articles_url = articles_url + params
    articles_json = requests.get(articles_url).json()
    articles = articles_json['articles']
    print(f'{source["name"]} article count: {len(articles)}')
    for article in articles:
        print(f'Title: {article["title"]}')


def scrape_articles_from_websites():
    sources = [Source(source) for source in config['sources']]
    with Pool(4) as pool:
        pool.map(import_articles, sources)
    print('\nFinished processing all sources.')


if __name__ == '__main__':
    import_articles_from_api()
    # scrape_articles_from_websites()
