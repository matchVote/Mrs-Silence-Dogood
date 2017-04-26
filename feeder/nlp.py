AVERAGE_READING_SPEED = 275  # WPM


def process(article):
    """Executes all NLP methods.

    :param article: ArticleAdapter - article data
    :returns: ArticleAdapter - set with extracted data from NLP
    """
    article.nlp()
    article.read_time = calculate_read_time(article.text)
    return article


def calculate_read_time(text):
    """Calculates the average reading time for the text of an article.

    :param text: str - article text
    :returns: int - average reading time in minutes rounded up
    """
    word_count = len(text.split(' '))
    return round(word_count / AVERAGE_READING_SPEED)
