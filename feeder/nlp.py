import re
from feeder.models import Official

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
    return round(word_count / AVERAGE_READING_SPEED)


def extract_mentioned_officials(text):
    """Finds all instances of last names of officials listed in text.

    :param text: str - article text
    :returns: list[str] - officials' last names
    """
    pattern = r'\W'
    last_names = official_names()
    res = [word for word in re.split(pattern, text) if word in last_names]
    print(res)
    return res


def official_names():
    """Returns a list of last names for all known officials.

    :returns: list[str] - list of last names
    """
    reps = Official.select(Official.first_name, Official.last_name)
    return [rep.last_name for rep in reps]
