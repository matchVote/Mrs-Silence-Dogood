from datetime import datetime
from peewee import IntegrityError
import pytest

from feeder.models import Article
from tests import transaction


class TestArticle(object):
    """Test cases for Article model."""

    def test_article_model_works(self, transaction):
        published = datetime.now()
        article = Article.create(
            url='http://bomb.sauce',
            title='CNN is Great',
            read_time=12,
            publisher='cnn',
            authors=['Ben', 'Bernanke'],
            date_published=published)

        assert article.url == 'http://bomb.sauce'
        assert article.title == 'CNN is Great'
        assert article.read_time == 12
        assert article.publisher == 'cnn'
        assert article.date_published == published
        assert len(article.authors) == 2
        assert article.created_at is not None

    def test_url_is_required(self, transaction):
        with pytest.raises(IntegrityError):
            Article.create(url=None, publisher='test')

    def test_publisher_is_required(self, transaction):
        with pytest.raises(IntegrityError):
            Article.create(publisher=None, url='test.com')
