import os
import yaml
from peewee import PostgresqlDatabase

env = os.environ.get('FEEDER_ENV', 'dev')
with open('database_config.yml') as f:
    config = yaml.load(f.read())[env]

db = PostgresqlDatabase(
    config['database'],
    user=config['user'],
    password=config['password'],
    host=config['host'],
    port=config['port'],
)
