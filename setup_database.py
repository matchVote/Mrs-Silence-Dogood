import os
from peewee import OperationalError, ProgrammingError

from feeder import db, config, PostgresqlDatabase
from feeder.article import Article

# Check if DB exists and create it if it doesn't
try:
    db.connect()
except OperationalError:
    os.system(f'createdb -h {config["host"]} -U {config["user"]} {config["database"]}')

try:
    db.create_tables([Article])
except ProgrammingError:
    pass # tables already exist
