import os
import yaml
from playhouse.postgres_ext import PostgresqlExtDatabase

env = os.environ.get('FEEDER_ENV', 'dev')
with open('config/database.yml') as f:
    config = yaml.load(f.read())[env]

db = PostgresqlExtDatabase(
    config['database'],
    user=config['user'],
    password=config['password'],
    host=config['host'],
    port=config['port'])
