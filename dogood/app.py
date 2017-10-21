import os
from string import Template
import yaml

from dogood.adapters import APISourceAdapterFactory
from dogood.apis import APIImporter
from dogood.scraping import scrape_sources
from dogood.utils import timer

with open('config/sources.yml') as f:
    config_template = Template(f.read())
    config_string = config_template.safe_substitute(os.environ)
    config = yaml.load(config_string)


def main():
    if os.environ.get('SCRAPING_IMPORT') == 'true':
        with timer('Scraping', 'importing...'):
            scrape_html_articles()

    if os.environ.get('API_IMPORT') == 'true':
        with timer('API', 'importing...'):
            import_articles_from_apis()


def scrape_html_articles():
    for source in config['sources']:
        # articles = scrape_source(source)
        # repo = Repo(Article)
        # old_articles = repo.select('url').where(publisher=source['publisher'])
        articles.remove(old_articles).limit(25).download().parse().enrich()
        # repo.insert(articles)
    print('\nFinished processing all scraped sources.')


def import_articles_from_apis():
    for api in config['apis']:
        adapter = APISourceAdapterFactory.create_adapter(api)
        APIImporter(adapter).import_articles()
    print('Finished processing all API articles.')


if __name__ == '__main__':
    main()
