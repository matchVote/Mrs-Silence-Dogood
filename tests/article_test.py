from datetime import datetime
from peewee import IntegrityError
import pytest

from feeder.article import Article
from tests import use_transaction


class TestArticle(object):
    """Test cases for Article model."""

    @use_transaction
    def test_article_model_works(self):
        published = datetime.now()
        article = Article.create(
            url='http://bomb.sauce',
            title='CNN is Great',
            read_time=12,
            publisher='cnn',
            authors=['Ben', 'Bernanke'],
            date_published=published,)

        assert article.url == 'http://bomb.sauce'
        assert article.title == 'CNN is Great'
        assert article.read_time == 12
        assert article.publisher == 'cnn'
        assert article.date_published == published
        assert len(article.authors) == 2
        assert article.created_at is not None

    @use_transaction
    def test_url_is_required(self):
        with pytest.raises(IntegrityError):
            Article.create(url=None, publisher='test')

    @use_transaction
    def test_publisher_is_required(self):
        with pytest.raises(IntegrityError):
            Article.create(publisher=None, url='test.com')
