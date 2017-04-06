from feeder.article import Article, create_table


class TestArticle(object):
    """Test cases for Article model."""

    @classmethod
    def setup_class(cls):
        """Creates article table."""
        create_table()

    def test_title_returns_title_of_article(self):
        article = Article.create(title='CNN is Great')
        assert article.title == 'CNN is Great'
