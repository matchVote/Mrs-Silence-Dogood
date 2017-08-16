from multiprocessing import Pool
import os
from string import Template
import yaml

from feeder.apis import APISourceAdapterFactory, APIImporter
from feeder.consume import import_articles
from feeder.source import Source

with open('config/sources.yml') as f:
    config_template = Template(f.read())
    config_string = config_template.safe_substitute(os.environ)
    config = yaml.load(config_string)


def import_articles_from_apis():
    print('Importing API sources...')
    for api in config['apis']:
        adapter = APISourceAdapterFactory.create_adapter(api)
        APIImporter(adapter).import_articles()
    print('\nFinished processing all API sources.')


def scrape_articles_from_websites():
    sources = [Source(source) for source in config['sources']]
    with Pool(4) as pool:
        pool.map(import_articles, sources)
    print('\nFinished processing all sources.')


if __name__ == '__main__':
    import_articles_from_apis()
    # scrape_articles_from_websites()
