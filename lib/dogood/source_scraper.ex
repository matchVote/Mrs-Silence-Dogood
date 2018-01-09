defmodule Dogood.SourceScraper do
  require Logger
  use Task

  def start_link(source) do
    Task.start_link(__MODULE__, :scrape, [source])
  end

  def scrape(%{url: url, publisher: publisher} = source) do
    # Logger.info("Scraping source #{publisher}...")
    # download html
    # extract all links
    # filter links
    # give each link to an ArticleScraper
  end
end
