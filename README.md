# Mrs. Silence Dogood
Consumes news articles to populate data for the news feed.

### Development Setup
    bin/build                 # builds containers
    bin/setup                 # prepares DB for DEV and TEST environments
    docker-compose up dogood  # starts containers and turns on dogood

### Testing
    bin/test  # runs tests

### Deployment
    bin/deploy

#### Update version
* setup.py

### TODO
* Increase test coverage
* URLFilterTest -- random test fails on the small chance of getting the same sets
  --randomly-seed=1509673345
