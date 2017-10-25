import logging
import os
from string import Template
import yaml

from peewee import IntegrityError

from dogood import Repo, URLFilter, nlp
from dogood.adapters import APISourceAdapterFactory, ArticleDecorator
from dogood.apis import APIImporter
from dogood.models import Article, ArticleOfficial, Official
from dogood.scraping import scrape_articles, scrape_source
from dogood.utils import timer

log = logging.getLogger(__name__)
log.setLevel = logging.INFO


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
        repo = Repo(Article)
        old_articles = repo.select('url').where(publisher=source['publisher'])
        existing_urls = {article.url for article in old_articles}
        log.info(f'Scraping source: {source["publisher"]}')
        article_urls = scrape_source(source)
        log.info(f'Scraped {len(article_urls)} articles urls')
        url_filter = URLFilter(article_urls, maximum=25)
        log.info(f'Removing {len(existing_urls)} existing articles...')
        url_filter.remove(existing_urls)
        log.info(f'Scraping {len(url_filter.urls)} articles...')
        articles = scrape_articles(url_filter.urls)
        political_articles = filter_political_articles(articles, source)
        log.info(f'Removed {len(url_filter.urls) - len(political_articles)} non-political articles')
        log.info('Enriching articles...')
        enriched_articles = nlp.enrich(political_articles)
        log.info(f'Saving {len(enriched_articles)} articles...')
        try:
            repo.insert(enriched_articles)
        except IntegrityError:
            log.warning(f'Failed articles: {enriched_articles}')

        link_articles_to_officials(enriched_articles)
    print('\nFinished processing all scraped sources.')


def filter_political_articles(articles, source):
    return [ArticleDecorator(article, source['publisher'])
            for article in articles
            if nlp.ArticleClassifier(article).is_political]


def link_articles_to_officials(articles):
    link_repo = Repo(ArticleOfficial)
    official_repo = Repo(Official)
    for article in articles:
        official_names = nlp.extract_full_official_names(article)
        for first_name, last_name in official_names:
            officials = official_repo.select('id')
            official = officials.where(first_name=first_name, last_name=last_name)
            link_repo.insert(article_id=article.id, official_id=official.id)


def import_articles_from_apis():
    for api in config['apis']:
        adapter = APISourceAdapterFactory.create_adapter(api)
        APIImporter(adapter).import_articles()
    print('Finished processing all API articles.')


if __name__ == '__main__':
    main()
