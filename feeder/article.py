from datetime import datetime
from feeder import db
from peewee import CharField, Model, IntegerField, DateTimeField


class BaseModel(Model):
    class Meta:
        database = db


class Article(BaseModel):
    """ORM model for articles table."""

    url = CharField(primary_key=True)
    brand = CharField()
    title = CharField(null=True)
    author = CharField(null=True)
    publisher = CharField(null=True)
    date_published = DateTimeField(null=True)
    read_time = IntegerField(null=True)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        db_table = 'articles'
