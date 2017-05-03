import os
import pytest

import newspaper
from feeder import nlp
from feeder.source import ArticleAdapter
from feeder.models import Official
from tests import transaction


class TestNLP(object):
    """Test cases for performing natural language processing."""

    @pytest.fixture(autouse=True)
    def article(self):
        article = newspaper.Article(url='http://')
        article.is_downloaded = article.is_parsed = True
        article.title = 'Sample Text'
        with open(os.path.abspath('tests/support/sample_text.txt')) as f:
            article.text = f.read()
        self.article = ArticleAdapter(article)

    def test_process_sets_all_attributes_for_nlp(self):
        article = nlp.process(self.article)
        assert article.keywords
        assert article.summary
        assert article.read_time
        assert article.mentioned_officials

    def test_read_time_calculates_average_reading_time_for_text_in_minutes(self):
        read_time = nlp.calculate_read_time(self.article.text)
        assert read_time == 1

    def test_extract_mentioned_officials_returns_all_last_names_of_officials_in_text(self, transaction):
        reps = [{'first_name': 'Kurt', 'last_name': 'Gödel'},
                {'first_name': 'M.C.', 'last_name': 'Escher'},
                {'first_name': 'Johann', 'last_name': 'Bach'},
                {'first_name': 'Haruki', 'last_name': 'Murakami'}]
        Official.insert_many(reps).execute()

        officials = nlp.extract_mentioned_officials(self.article.text)
        assert officials == ['Kurt Gödel', 'M.C. Escher',
                             'Johann Bach', 'Haruki Murakami']
