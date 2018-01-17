defmodule Dogood.SourceScraper do
  require Logger
  use Task

  @pool_timeout 5000  # 5 seconds

  def start_link(source) do
    Task.start_link(__MODULE__, :scrape, source)
  end

  def scrape(%{"url" => url, "publisher" => publisher}) do
    Logger.info("Scraping source #{publisher}...")
    url
    |> request_source()
    |> extract_anchor_urls()
    |> filter_urls()
    |> scrape_articles(publisher)
  end

  defp request_source(url) do
    %{body: html} = HTTPoison.get!(url)
    html
  end

  def extract_anchor_urls(html) do
    html
    |> Floki.find("a")
    |> Enum.flat_map(fn({_, attrs, _}) ->
      case Enum.find(attrs, fn({key, _}) -> key == "href" end) do
        {"href", url} -> [url]
        _ -> []
      end
    end)
  end

  def filter_urls(urls) do
    urls
  end

  def scrape_articles(urls, publisher) do
    IO.puts "Sending #{length urls} urls from #{publisher} to ArticleScrapers"
    Enum.each urls, fn(url) ->
      message = {:scrape, {url, publisher}}
      :"article_scraper_pool #{publisher}"
      |> :poolboy.transaction(&(GenServer.cast(&1, message)), @pool_timeout)
    end
  end
end
