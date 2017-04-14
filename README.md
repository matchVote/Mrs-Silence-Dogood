# News Feeder
Consumes news articles to populate data for the news feed.

### Development Setup
    bin/build                 # builds containers
    bin/setup                 # prepares DB
    docker-compose up feeder  # starts containers and turns on feeder

### Test Setup
    bin/setup test  # prepares DB for test env
    bin/test        # runs tests

#### Notes
Articles:  
* For consideration:
  * Move the following to the web app:
  * upvote_downvote_count
  * most_read
  * bookmark_status
