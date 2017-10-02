from itertools import chain
import logging
import re

from dogood import repo
from dogood.models import ArticleOfficial, Official

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

AVERAGE_READING_SPEED = 275  # WPM


class NLProcessor:
    """Natural language processing operations on an article."""

    def __init__(self, article):
        self.article = article
        self.officials_first_names = set()
        self.officials_last_names = set()

    def process_article(self):
        self.set_keywords_and_summary()
        self.set_read_time()
        self.associate_to_mentioned_officials()

    def set_keywords_and_summary(self):
        self.article.nlp()  # newspaper.Article method

    def set_read_time(self):
        """Calculates the average reading time for the text of an article.
        Read time is in minutes rounded up.
        """
        word_count = len(self.article.text.split(' '))
        time = round(word_count / AVERAGE_READING_SPEED)
        if not time:
            time = 1
        self.article.read_time = time

    def associate_to_mentioned_officials(self):
        self.extract_names_of_officials()
        self.link_articles_to_officials()

    def extract_names_of_officials(self):
        names = official_name_mapping()
        words = re.split(r'\W', self.article.text)
        for index, word in enumerate(words):
            first_name = names.get(word, False)
            if first_name:
                if words[index-1] == first_name:
                    self.officials_first_names.add(first_name)
                    self.officials_last_names.add(word)

    def link_articles_to_officials(self):
        officials = repo.official_ids_by_first_and_last_names(
            self.officials_first_names,
            self.officials_last_names)
        self.article.mentioned_officials = officials

    def classify_article(self):
        names = set(officials_names())
        words = set(self.article.text.split(' '))
        if names & words:
            return 'politics'


def officials_names():
    officials = repo.select_first_and_last_name_from_officials()
    return chain.from_iterable((o.first_name, o.last_name) for o in officials)


def official_name_mapping():
    officials = repo.select_first_and_last_name_from_officials()
    return {official.last_name: official.first_name for official in officials}
