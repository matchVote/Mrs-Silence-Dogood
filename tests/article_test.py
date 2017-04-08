from datetime import datetime
import pytest
from peewee import IntegrityError

from feeder.article import Article
from tests import transaction


class TestArticle(object):
    """Test cases for Article model."""

    @transaction
    def test_article_model_works(self):
        article = Article.create(
            url='http://bomb.sauce',
            title='CNN is Great',
            read_time=12,
            brand='cnn',
            date_published=datetime.now(),
        )
        assert article.url == 'http://bomb.sauce'
        assert article.title == 'CNN is Great'
        assert article.author is None
        assert article.read_time == 12
        assert article.brand == 'cnn'
        assert article.date_published is not None

    @transaction
    def test_url_is_required(self):
        with pytest.raises(IntegrityError):
            Article.create(url=None, brand='test')

    @transaction
    def test_brand_is_required(self):
        with pytest.raises(IntegrityError):
            Article.create(brand=None, url='test.com')
