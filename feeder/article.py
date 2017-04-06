from feeder import db
from peewee import CharField, Model, OperationalError


class BaseModel(Model):
    class Meta:
        database = db


class Article(BaseModel):
    """ORM model for articles table."""

    title = CharField()


def create_table():
    try:
        Article.create_table()
    except OperationalError:
        print('Articles table already exists!')
