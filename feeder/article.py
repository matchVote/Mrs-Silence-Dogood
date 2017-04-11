from datetime import datetime
from feeder import db
from peewee import CharField, Model, IntegerField, DateTimeField
from playhouse.postgres_ext import ArrayField


class BaseModel(Model):
    class Meta:
        database = db


class Article(BaseModel):
    """ORM model for articles table."""

    url = CharField(primary_key=True)
    title = CharField(null=True)
    authors = ArrayField(field_class=CharField, null=True)
    publisher = CharField()
    date_published = DateTimeField(null=True)
    read_time = IntegerField(null=True)
    keywords = ArrayField(field_class=CharField, null=True)
    summary = CharField(null=True)
    mentioned_officials = ArrayField(field_class=CharField, null=True)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        db_table = 'articles'
