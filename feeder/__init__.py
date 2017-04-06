from peewee import PostgresqlDatabase

config = dict(database='feeder_dev',
              user='postgres',
              password='postgres',
              host='postgres',
              port=5432)

db = PostgresqlDatabase(
    config['database'],
    user=config['user'],
    password=config['password'],
    host=config['host'],
    port=config['port'],
)
