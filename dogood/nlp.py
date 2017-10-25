import logging
import re

from dogood import Repo
from dogood.models import Official

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

AVERAGE_READING_SPEED = 275  # WPM


class ArticleClassifier:
    """Determine the category in which an article falls."""

    def __init__(self, article):
        self.classification = None
        self.classify(article)

    def classify(self, article):
        names = extract_full_official_names(article)
        for name in names:
            name = ' '.join(name)
            if article.text.find(name) != -1:
                self.classification = 'politics'
                break

    def is_political(self):
        return self.classification == 'politics'


def extract_full_official_names(article):
    names = official_name_mapping()
    words = re.split(r'\W', article.text)
    full_names = []
    for index, word in enumerate(words):
        first_name = names.get(word, False)
        if first_name:
            if words[index-1] == first_name:
                full_names.append((first_name, word))
    return full_names


def official_name_mapping():
    repo = Repo(Official)
    officials = repo.select('first_name', 'last_name')
    return {official.last_name: official.first_name for official in officials}


def enrich(articles):
    for article in articles:
        extract_keywords_and_summary(article)
        calculate_read_time(article)
    return articles


def extract_keywords_and_summary(article):
    article.nlp()  # newspaper.Article method


def calculate_read_time(article):
    """Calculates the average reading time for the text of an article.
    Read time is in minutes rounded up.
    """
    word_count = len(article.text.split(' '))
    time = round(word_count / AVERAGE_READING_SPEED)
    article.read_time = time or 1


# class NLProcessor:
#     """Natural language processing operations on an article."""
#
#     def __init__(self, article):
#         self.article = article
#         self.officials_first_names = set()
#         self.officials_last_names = set()
#
#     def process_article(self):
#         self.set_keywords_and_summary()
#         self.set_read_time()
#         self.associate_to_mentioned_officials()
#
#     def set_keywords_and_summary(self):
#         self.article.nlp()  # newspaper.Article method
#
#     def set_read_time(self):
#         """Calculates the average reading time for the text of an article.
#         Read time is in minutes rounded up.
#         """
#         word_count = len(self.article.text.split(' '))
#         time = round(word_count / AVERAGE_READING_SPEED)
#         if not time:
#             time = 1
#         self.article.read_time = time
#
#     def associate_to_mentioned_officials(self):
#         self.extract_names_of_officials()
#         self.link_articles_to_officials()
#
#     def extract_names_of_officials(self):
#         names = official_name_mapping()
#         words = re.split(r'\W', self.article.text)
#         for index, word in enumerate(words):
#             first_name = names.get(word, False)
#             if first_name:
#                 if words[index-1] == first_name:
#                     self.officials_first_names.add(first_name)
#                     self.officials_last_names.add(word)
#
#     def link_articles_to_officials(self):
#         officials = repo.official_ids_by_first_and_last_names(
#             self.officials_first_names,
#             self.officials_last_names)
#         self.article.mentioned_officials = officials
#
#
