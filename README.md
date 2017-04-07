# News Feeder
Consumes news articles to populate data for the news feed.

### Development Setup
    bin/build                 # builds containers
    bin/setup                 # prepares DB
    docker-compose up feeder  # starts containers

### Test Setup
    bin/setup test  # prepares DB for test env
    bin/test        # runs tests

#### Notes
Articles:  
* url - primary key
* title
* author
* publisher
* date_published
* read_time
* keywords - array
* summary - array
* mentioned_officials
* topics

For consideration:
* upvote_downvote_count
* most_read
* bookmark_status
