import pytest

from dogood import Repo
from dogood.models import Article


@pytest.fixture
def repo():
    return Repo(Article)


@pytest.fixture
def articles():
    return [
        dict(url='new1', title='new1 title', publisher='Somebody'),
        dict(url='new2', title='new2 title', publisher='Somebody'),
        ]


class TestRepo:

    @classmethod
    def setup_class(cls):
        with Article._meta.database.atomic():
            Article.insert_many([
                dict(url='hey.com', publisher='ABC News', title='Awesome'),
                dict(url='there.com', publisher='ABC News', title='Tubular'),
            ]).execute()

    @classmethod
    def teardown_class(cls):
        Article.delete().execute()

    def test_select_with_no_arguments(self, repo):
        articles = repo.select()
        assert ['hey.com', 'there.com'] == [article.url for article in articles]
        assert ['Awesome', 'Tubular'] == [article.title for article in articles]

    def test_select_with_one_argument(self, repo):
        articles = repo.select('url')
        assert ['hey.com', 'there.com'] == [article.url for article in articles]
        assert [None, None] == [article.title for article in articles]

    def test_select_with_multiple_arguments(self, repo):
        articles = repo.select('url', 'publisher')
        results = [(article.url, article.publisher) for article in articles]
        assert [('hey.com', 'ABC News'), ('there.com', 'ABC News')] == results

    def test_select_resets_the_query(self, repo):
        article = repo.select('url').select('title')[0]
        assert article.title
        assert not article.url
        articles = repo.select('url').where(title='Awesome')
        assert len(articles) == 1
        articles = repo.select().where(publisher='ABC News')
        assert len(articles) == 2

    def test_filtering_a_select_with_a_where_clause(self, repo):
        articles = repo.select('url').where(title='Awesome')
        assert len(articles) == 1

    def test_bulk_inserting_articles(self, repo, articles):
        repo.insert(articles)
        assert len(repo.select()) == 4
        cleanup_by_publisher(articles[0]['publisher'])


def cleanup_by_publisher(publisher):
    Article.delete().where(Article.publisher == publisher).execute()
