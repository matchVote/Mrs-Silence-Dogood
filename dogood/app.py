from multiprocessing import Pool
import os
from string import Template
import yaml

from dogood import timer
from dogood.adapters import APISourceAdapterFactory
from dogood.apis import APIImporter
from dogood.scraper import Scraper
from dogood.source import Source

with open('config/sources.yml') as f:
    config_template = Template(f.read())
    config_string = config_template.safe_substitute(os.environ)
    config = yaml.load(config_string)


def main():
    if os.environ.get('API_IMPORT') == 'true':
        with timer('API', 'importing...'):
            import_articles_from_apis()

    if os.environ.get('SCRAPING_IMPORT') == 'true':
        with timer('Scraping', 'importing...'):
            scrape_articles_from_websites()


def import_articles_from_apis():
    for api in config['apis']:
        adapter = APISourceAdapterFactory.create_adapter(api)
        APIImporter(adapter).import_articles()
    print('Finished processing all API articles.')


def scrape_articles_from_websites():
    sources = (Source(source) for source in config['sources'])
    worker_count = int(os.environ.get('WORKER_POOL_MAX', 1))
    with Pool(worker_count) as pool:
        pool.map(scrape_articles, sources)
    print('\nFinished processing all scraped sources.')


def scrape_articles(source):
    Scraper(source).execute()


if __name__ == '__main__':
    main()
