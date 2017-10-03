import pytest

from dogood.nlp import ArticleClassifier
from tests.support.helpers import MockArticle


@pytest.fixture
def political_article():
    with open('tests/support/sample_text.txt') as f:
        return MockArticle(text=f.read())


@pytest.fixture
def non_political_article():
    return MockArticle(text='this has nothing to do with politics')


class TestArticleClassifier:

    def test_is_political_returns_true_if_text_contains_official_names(self, political_article):
        classifier = ArticleClassifier(political_article)
        assert classifier.is_political()

    def test_is_political_returns_false_if_text_does_not_contain_official_names(self, non_political_article):
        classifier = ArticleClassifier(non_political_article)
        assert not classifier.is_political()
