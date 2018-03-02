defmodule Dogood.PublisherScraper do
  use Task
  require Logger

  @worker_count Application.get_env(:dogood, :article_scrapers_per_source)

  def start_link(%{"url" => url, "publisher" => publisher}) do
    Task.start_link(__MODULE__, :scrape, [url, publisher])
  end

  def scrape(url, publisher) do
    url
    |> parse_article_urls()
    |> filter_urls()
    |> scrape_articles(publisher)
  end

  def parse_article_urls(url) do
    case Dogood.NLP.parse_source(url) do
      {:ok, urls} -> urls
      _ -> []
    end
  end

  def filter_urls([]), do: nil
  def filter_urls(urls) do
    urls
    |> Enum.uniq()
    |> Enum.filter(&String.ends_with?(&1, ".html"))
  end

  def scrape_articles(nil, _), do: Dogood.Foreman.publisher_finished
  def scrape_articles(urls, publisher) do
    Logger.info("Scraping #{length urls} urls from #{publisher}.")
    scraped_count =
      concurrent_stream(urls, publisher)
      |> Enum.to_list
      |> length
    Logger.info("#{scraped_count} articles scraped.")
    Dogood.Foreman.publisher_finished
  end

  def concurrent_stream(urls, publisher) do
    Task.Supervisor.async_stream_nolink(
      :"article_scraper_supervisor-#{publisher}",
      urls,
      &Dogood.ArticleScraper.scrape(&1, publisher),
      max_concurrency: @worker_count,
      ordered: false,
      timeout: 15_000
    )
  end
end
