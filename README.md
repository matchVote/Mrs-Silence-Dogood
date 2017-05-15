# News Feeder
Consumes news articles to populate data for the news feed.

### Development Setup
    bin/build                 # builds containers
    bin/setup                 # prepares DB for DEV and TEST environments
    docker-compose up feeder  # starts containers and turns on feeder

### Testing 
    bin/test  # runs tests

#### Notes
* Move the following to the web app:
  * newsworthiness_count
  * most_read
  * bookmark_status
