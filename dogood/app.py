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
MAX_ARTICLES_PER_SOURCE = int(os.getenv('MAX_ARTICLES_PER_SOURCE'))


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
    repo = Repo(Article)
    for source in config['sources']:
        old_articles = repo.select('url').where(publisher=source['publisher'])
        existing_urls = {article.url for article in old_articles}
        article_urls = scrape_source(source)
        political_articles = filter_political_articles(article_urls, existing_urls, source)
        if political_articles:
            enriched_articles = nlp.enrich(political_articles)
            log.info(f'Saving {len(enriched_articles)} political articles...')
            repo.insert(enriched_articles)
            link_articles_to_officials(enriched_articles, repo)
    print('\nFinished processing all scraped sources.')


def filter_political_articles(article_urls, urls_to_remove, source):
    political_articles = []
    while len(political_articles) == 0:
        url_filter = URLFilter(article_urls, maximum=MAX_ARTICLES_PER_SOURCE)
        url_filter.remove(urls_to_remove)
        articles = scrape_articles(url_filter.urls)
        political_articles = [ArticleDecorator(article, source['publisher'])
                              for article in articles
                              if nlp.ArticleClassifier(article).is_political()]
        urls_to_remove |= url_filter.urls
        if urls_to_remove == set(article_urls):
            break
    return political_articles


def link_articles_to_officials(articles, article_repo):
    link_repo = Repo(ArticleOfficial)
    official_repo = Repo(Official)
    for article in articles:
        article_id = article_repo.select('id').where(url=article.url)[0].id
        official_names = nlp.extract_full_official_names(article)
        for first_name, last_name in official_names:
            officials = official_repo.select('id')
            official = officials.where(first_name=first_name, last_name=last_name)[0]
            record = {'article_id': article_id, 'representative_id': official.id}
            try:
                link_repo.insert([record])
            except IntegrityError:
                pass


def import_articles_from_apis():
    for api in config['apis']:
        adapter = APISourceAdapterFactory.create_adapter(api)
        APIImporter(adapter).import_articles()
    print('Finished processing all API articles.')


if __name__ == '__main__':
    main()
