defmodule Dogood.SourceScraper do
  require Logger
  use Task

  def start_link(source) do
    Task.start_link(__MODULE__, :scrape, [source])
  end

  def scrape(%{url: url, publisher: publisher} = source) do
    Logger.info("Scraping source #{publisher}...")
    url
    |> request_source()
    |> extract_anchor_urls()
    |> filter_urls()
    |> scrape_articles()
  end

  defp request_source(url) do
    %{body: html} = HTTPoison.get!(url)
    html
  end

  def extract_anchor_urls(html) do
    html
    |> Floki.find("a")
    |> Enum.map(fn({_, attrs, _}) ->
      {"href", url} = Enum.find(attrs, fn({key, value}) -> key == "href" end)
      url
    end)
  end

  def filter_urls(urls) do
    urls
  end

  def scrape_articles(urls) do
end
end
