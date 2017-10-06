from datetime import datetime

from peewee import IntegrityError
import pytest

from dogood.models import Article


@pytest.mark.usefixtures('transaction')
class TestArticle:
    """Test cases for Article model."""

    def test_article_model_works(self):
        published = datetime.now()
        article = Article.create(
            url='http://bomb.sauce',
            title='CNN is Great',
            read_time=12,
            publisher='cnn',
            authors=['Ben', 'Bernanke'],
            top_image_url='http://some_image.com/link.pic',
            date_published=published)

        assert article.url == 'http://bomb.sauce'
        assert article.title == 'CNN is Great'
        assert article.read_time == 12
        assert article.publisher == 'cnn'
        assert article.date_published == published
        assert len(article.authors) == 2
        assert article.created_at is not None
        assert article.top_image_url == 'http://some_image.com/link.pic'

    def test_url_is_required(self):
        with pytest.raises(IntegrityError):
            Article.create(url=None, publisher='test')

    def test_publisher_is_required(self):
        with pytest.raises(IntegrityError):
            Article.create(publisher=None, url='test.com')
