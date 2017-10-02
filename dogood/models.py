from datetime import datetime
from peewee import TextField, Model, IntegerField, DateTimeField
from playhouse.postgres_ext import ArrayField

from dogood import db


class BaseModel(Model):
    class Meta:
        database = db


class Article(BaseModel):
    """ORM model for articles table."""

    url = TextField(unique=True)
    title = TextField(null=True)
    authors = ArrayField(field_class=TextField, null=True)
    publisher = TextField()
    date_published = DateTimeField(null=True)
    keywords = ArrayField(field_class=TextField, null=True)
    summary = TextField(null=True)
    read_time = IntegerField(null=True)
    top_image_url = TextField(null=True)
    source = TextField(null=True)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        db_table = 'articles'


class Official(BaseModel):
    """ORM model for representatives table."""

    first_name = TextField()
    last_name = TextField()
    middle_name = TextField(null=True)
    official_full_name = TextField(null=True)

    class Meta:
        db_table = 'representatives'


class ArticleOfficial(BaseModel):
    """Join table for articles and officials."""

    article_id = IntegerField()
    official_id = IntegerField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        db_table = 'articles_officials'
