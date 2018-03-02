# Mrs. Silence Dogood
Consumes news articles to populate data for the news feed.

### Development Setup
    bin/build                 # builds containers
    bin/setup                 # prepares DB for DEV and TEST environments
    docker-compose up dogood  # starts containers and turns on dogood

### Testing
Run all tests: `bin/test`  
Run one test file: `bin/test path/to/test.exs`

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



#### Workflow
* source{:url, :publisher}
* NLP/parse_source
  * download source html
  * extract article urls
* filter urls
* for url in urls
  * download article html
  * NLP/extract
    * extract article text
    * extract article title
  * classify text -> NLP/classify
  * filter out articles not political
  * analyze text -> NLP/analyze
  * insert article
  * for mentioned official
    * insert article official link
