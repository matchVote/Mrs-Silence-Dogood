class ArticleAdapter(object):
    """Wraps downloaded article data.

    This represents the boundary between external article data and the rest of
    the system, maintaining a standard interface for further processing.
    """

    def __init__(self, article):
        """This expects a newspaper.Article object.

        :param article: newspaper.Article - object containing downloaded article
        """
        self.external_article = article
        self.read_time = 0
        self.mentioned_officials = []

    def __getattr__(self, name):
        """If attribute is not found on adapter, delegate to external article."""
        return getattr(self.external_article, name)

    def nlp(self):
        """Delegation method to newspaper.Article."""
        self.external_article.nlp()
