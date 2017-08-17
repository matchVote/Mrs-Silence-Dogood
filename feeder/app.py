from multiprocessing import Pool
import os
from string import Template
import yaml

from feeder.adapters import APISourceAdapterFactory
from feeder.consume import APIImporter, import_articles
from feeder.source import Source

with open('config/sources.yml') as f:
    config_template = Template(f.read())
    config_string = config_template.safe_substitute(os.environ)
    config = yaml.load(config_string)


def import_articles_from_apis():
    for api in config['apis']:
        adapter = APISourceAdapterFactory.create_adapter(api)
        APIImporter(adapter).import_articles()
    print('Finished processing all API articles.')


def scrape_articles_from_websites():
    sources = [Source(source) for source in config['sources']]
    with Pool(4) as pool:
        pool.map(import_articles, sources)
    print('\nFinished processing all scraped sources.')


if __name__ == '__main__':
    print('\nImporting API articles...')
    import_articles_from_apis()
    print('\nImporting scraped sources...')
    scrape_articles_from_websites()
