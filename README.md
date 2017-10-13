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
* Exception that crashes the process still leaves container running, so it 
won't restart in ECS
* Clean up NLProcessor
* Increase test coverage
