from feeder import nlp, timer
from feeder.models import Article


def import_articles(source):
    """Downloads, parses, transforms, and persists article data.

    :param source: Source - url and publisher of a source of articles
    """
    source.build(ignore=existing_article_urls(source.publisher))
    with timer('Processing articles...'):
        for article in source.articles:
            persist(map_article(nlp.process(parse(article))))


def existing_article_urls(publisher):
    """Returns URLs for previously imported articles for publisher.

    :param publisher: str - article publisher
    :returns: list[str] - urls for existing articles
    """
    articles = Article.select(Article.url).filter(Article.publisher == publisher)
    return [article.url for article in articles]


def parse(article):
    """Parses raw HTML into data attributes.

    :param article: ArticleAdapter - article object containing raw HTML
    :returns: ArticleAdapter - article object with parsed attributes
    """
    article.parse()
    return article


def map_article(article):
    """Converts parsed data into an acceptable format for the Article model.

    :param article: object - container of parsed data
    :returns: dict - article data
    """
    return {
        'publisher': article.publisher,
        'url': article.url,
        'authors': article.authors,
        'title': article.title,
        'date_published': article.publish_date,
        'keywords': article.keywords,
        'summary': article.summary,
        'read_time': article.read_time,
        'mentioned_officials': article.mentioned_officials
    }


def persist(data):
    """Stuffs data into Article model and saves to database.

    :param data: dict - article data
    """
    Article.create(**data)
