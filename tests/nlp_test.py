import os
import pytest

import newspaper
from feeder import nlp
from feeder.adapters import ArticleAdapter


class TestNLP(object):
    """Test cases for performing natural language processing."""

    def setup_method(self, _method):
        self.parsed_article = ArticleAdapter(setup_external_article())

    def test_process_sets_all_attributes_for_nlp(self):
        article = nlp.process(self.parsed_article)
        assert article.keywords
        assert article.summary
        assert article.read_time
        # assert article.mentioned_officials

    def test_read_time_calculates_average_reading_time_for_text(self):
        read_time = nlp.calculate_read_time(self.parsed_article.text)
        assert read_time == 1


def setup_external_article():
    article = newspaper.Article(url='http://')
    article.is_downloaded = article.is_parsed = True
    article.title = 'Sample Text'
    with open(os.path.abspath('tests/support/sample_text.txt')) as f:
        article.text = f.read()
    return article
