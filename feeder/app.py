from multiprocessing import Pool
import yaml

from feeder.consume import import_articles
from feeder.source import Source

with open('config/sources.yml') as f:
    config = yaml.load(f)

if __name__ == '__main__':
    sources = [Source(source) for source in config['sources']]
    with Pool(4) as pool:
        pool.map(import_articles, sources)
    print('\nFinished processing all sources.')
