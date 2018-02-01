# Mrs. Silence Dogood
Consumes news articles to populate data for the news feed.

### Development Setup
    bin/build                 # builds containers
    bin/setup                 # prepares DB for DEV and TEST environments
    docker-compose up dogood  # starts containers and turns on dogood

### Testing
    bin/test  # runs tests

#### TODO
* articles.date_published is not being captured
* Test error handling when NLP service is unresponsive

#### Update version
* mix.exs

#### Process Design
                       Supervisor
                           |
                  ___________________
                 |                   |
         ScrapingSupervisor       Foreman
                 |          
    PublisherScraperSupervisor..N
                 |
          ________________
         |                |
 PublisherScraper   ArticleScraperSupervisor
                          |
                    ArticleScraper..5
