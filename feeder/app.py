import yaml
from feeder.consume import import_articles

with open('config/sources.yml') as f:
    config = yaml.load(f)
    base = config['base']
    sources = config['sources']

if __name__ == '__main__':
    for source in sources:
        import_articles(base + source)
