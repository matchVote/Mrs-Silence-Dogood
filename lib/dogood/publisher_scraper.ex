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
      _ -> nil
    end
  end

  def filter_urls(nil), do: nil

  def filter_urls(urls) do
    urls
    |> Enum.uniq()
    |> Enum.filter(&String.ends_with?(&1, ".html"))
  end

  def scrape_articles(nil, publisher) do
    Dogood.Foreman.publisher_finished(publisher)
  end

  def scrape_articles(urls, publisher) do
    Logger.info("Scraping #{length(urls)} urls from #{publisher}.")
    concurrent_stream(urls, publisher) |> Enum.to_list()
    Dogood.Foreman.publisher_finished(publisher)
  end

  def concurrent_stream(urls, publisher) do
    Task.Supervisor.async_stream_nolink(
      :"article_scraper_supervisor-#{publisher}",
      urls,
      &Dogood.ArticleScraper.scrape(&1, publisher),
      max_concurrency: @worker_count,
      ordered: false,
      timeout: 30_000
    )
  end
end
