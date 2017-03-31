from feeder.article import Article


class TestArticle(object):
    """Test cases for Article model."""

    def test_title_returns_title_of_article(self):
        article = Article.create(title='CNN is Great')
        assert article.title == 'CNN is Great'
