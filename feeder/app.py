import yaml
from feeder.consume import import_articles
from feeder.source import Source

with open('config/sources.yml') as f:
    config = yaml.load(f)

if __name__ == '__main__':
    for source in config['sources']:
        import_articles(Source(source))
