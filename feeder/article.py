from peewee import CharField, Model, OperationalError, SqliteDatabase

db = SqliteDatabase('feeder.db')


class Article(Model):
    """ORM model for articles table."""

    title = CharField()

    class Meta:
        database = db


if __name__ == '__main__':
    try:
        Article.create_table()
    except OperationalError:
        print('Articles table already exists!')
