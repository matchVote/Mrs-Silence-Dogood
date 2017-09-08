import logging
import re

from dogood import repo

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

AVERAGE_READING_SPEED = 275  # WPM


class NLProcessor:
    """Natural language processing operations on an article."""

    def __init__(self, article):
        self.article = article

    def classify_article(self):
        names = set(officials_names())
        words = set(self.article.text.split(' '))
        if names & words:
            return 'politics'

    def process_article(self):
        self.set_keywords_and_summary()
        self.set_read_time()
        self.set_mentioned_officials()

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

    def set_mentioned_officials(self):
        """Finds all instances of first and last names of officials listed in text.
        If only last name if found, it keeps that too.
        """
        mentions = set()
        names = official_name_mapping()
        words = re.split(r'\W', self.article.text)

        for index, word in enumerate(words):
            first_name = names.get(word, False)
            if first_name:
                if words[index-1] == first_name:
                    mentions.add(f'{first_name} {word}')
                else:
                    mentions.add(word)
        self.article.mentioned_officials = mentions


def officials_names():
    officials = repo.select_first_and_last_name_from_officials()
    names = []
    for official in officials:
        names.append(official.first_name)
        names.append(official.last_name)
    return names


def official_name_mapping():
    officials = repo.select_first_and_last_name_from_officials()
    return {official.last_name: official.first_name for official in officials}
