from collections import namedtuple

import pytest

from dogood.adapters import ArticleAdapter
from dogood.nlp import NLProcessor

MockArticle = namedtuple('MockArticle', 'text')


class TestNLProcessor:

    @pytest.fixture
    def processor(self):
        with open('tests/support/sample_text.txt') as f:
            article = ArticleAdapter(MockArticle(text=f.read()))
            processor = NLProcessor(article)
            processor.extract_names_of_officials()
            return processor

    def test_extract_names_of_officials_stores_first_names(self, processor):
        assert processor.officials_first_names == {'Bill', 'Tammy'}

    def test_extract_names_of_officials_stores_last_names(self, processor):
        assert processor.officials_last_names == {'Haslam', 'Duckworth'}

    def test_link_articles_to_officials_adds_official_models_to_article(self, processor):
        processor.link_articles_to_officials()
        officials = processor.article.mentioned_officials
        assert len(officials) == 2
