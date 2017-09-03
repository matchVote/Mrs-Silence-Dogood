import re
from dogood.models import Official

AVERAGE_READING_SPEED = 275  # WPM


def process(article):
    """Executes all NLP methods.

    :param article: ArticleAdapter - article data
    :returns: ArticleAdapter - set with extracted data from NLP
    """
    article.nlp()
    article.read_time = calculate_read_time(article.text)
    article.mentioned_officials = extract_mentioned_officials(article.text)
    return article


def calculate_read_time(text):
    """Calculates the average reading time for the text of an article.

    :param text: str - article text
    :returns: int - average reading time in minutes rounded up
    """
    word_count = len(text.split(' '))
    time = round(word_count / AVERAGE_READING_SPEED)
    if not time:
        time = 1
    return time


def extract_mentioned_officials(text):
    """Finds all instances of first and last names of officials listed in text.
    If only last name if found, it keeps that too.

    :param text: str - article text
    :returns: list[str] - officials' last names
    """
    mentions = set()
    names = official_names()
    words = re.split(r'\W', text)

    for index, word in enumerate(words):
        first_name = names.get(word, False)
        if first_name:
            if words[index-1] == first_name:
                mentions.add(f'{first_name} {word}')
            else:
                mentions.add(word)
    return mentions


def official_names():
    """Returns a list of last names for all known officials.

    :returns: list[str] - list of last names
    """
    reps = Official.select(Official.first_name, Official.last_name)
    return {rep.last_name: rep.first_name for rep in reps}
