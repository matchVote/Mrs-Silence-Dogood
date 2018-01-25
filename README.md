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
                  _____________
                 |             
       SourceScraperSupervisor..N
                 |
             ___________
            |           |
     SourceScraper   ArticleScraperSupervisor
                        |
                     ArticleScraper..5


Pooled SourceScraperSupervisor Design (Foreman controls pool)

                       Supervisor
                           |
                  ___________________
                 |                   |
        PublisherSupervisor       Foreman
                 |          
        ScraperSupervisor..N
                 |
             ___________
            |           |
     SourceScraper   ArticleScraperSupervisor
                        |
                     ArticleScraper..5
