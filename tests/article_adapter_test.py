import pytest
import newspaper

from feeder.article_adapter import ArticleAdapter


class TestArticleAdapter(object):
    """Test cases for ArticleAdapter."""

    def setup_method(self, _method):
        self.external_article = setup_external_article()

    def test_title_returns_original_title(self):
        article = ArticleAdapter(self.external_article)
        assert article.title == 'Original Title'


def setup_external_article():
    article = newspaper.Article(url='http://')
    article.title = 'Original Title'
    return article
