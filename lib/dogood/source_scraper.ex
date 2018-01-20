defmodule Dogood.SourceScraper do
  use Task, restart: :permanent

  require Logger
  alias Dogood.ArticleScraper

  @pool_timeout 300_000     # 5 minutes
  @source_cooldown 300_000  # 5 minutes

  def start_link(source) do
    Task.start_link(__MODULE__, :scrape_source, source)
  end

  def scrape_source(%{"url" => url, "publisher" => publisher}) do
    scrape(url, publisher)
    cooldown(publisher)
  end

  def scrape(source_url, publisher) do
    source_url
    |> parse_article_urls()
    |> filter_urls()
    |> scrape_articles(publisher)
  end

  def parse_article_urls(source_url), do: Dogood.NLP.parse_source(source_url)

  def filter_urls(urls) do
    urls
    |> Enum.uniq()
    |> Enum.filter(&String.ends_with?(&1, ".html"))
  end

  def scrape_articles(urls, publisher) do
    Logger.info("Scraping #{length urls} urls from #{publisher}...")
    Enum.each urls, fn(url) ->
      Task.start fn ->
        :poolboy.transaction(
          :"article_scraper_pool-#{publisher}",
          &ArticleScraper.scrape_article(&1, url, publisher),
          @pool_timeout
        )
      end
    end
  end

  defp cooldown(publisher) do
    Logger.info("Cooldown: #{publisher}")
    :timer.sleep(@source_cooldown)
  end
end
