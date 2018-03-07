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
                      _________|__________
                     |                    |
                  Scraper        ConsumerSupervisor



#### Current Workflow
for each publisher
  download |>
  extract_urls |>
  filter_urls -> article_urls
for each article_url
  download |>
  parse |>
  classify |>
  analyze |>
  persist, link_to_reps
