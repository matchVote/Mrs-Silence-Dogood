defmodule Dogood.SourceScraper do
  require Logger
  use Task, restart: :permanent

  @pool_timeout 5000        # 5 seconds
  @source_cooldown 300_000  # 5 minutes

  def start_link(source) do
    Task.start_link(__MODULE__, :scrape_source, source)
  end

  def scrape_source(%{"url" => url, "publisher" => publisher}) do
    scrape(url, publisher)
    cooldown(publisher)
  end

  def scrape(url, publisher) do
    url
    |> request_source()
    |> compile_urls(url)
    |> scrape_articles(publisher)
  end

  defp request_source(url) do
    %{body: html} = HTTPoison.get!(url)
    html
  end

  def compile_urls(html, source_url) do
    html
    |> extract_anchor_urls()
    |> add_prefix(source_url)
    |> filter_urls()
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

  def add_prefix(urls, source_url) do
    prefix = parse_domain(source_url)
    Enum.map urls, fn(url) ->
      if String.starts_with?(url, "/"), do: prefix <> url, else: url
    end
  end

  defp parse_domain(url) do
    url
    |> String.split("/")
    |> Enum.slice(0..2)
    |> Enum.join("/")
  end

  def filter_urls(urls) do
    urls
    |> Enum.uniq()
    |> Enum.filter(&String.ends_with?(&1, ".html"))
  end

  def scrape_articles(urls, publisher) do
    Logger.info("Scraping #{length urls} urls from #{publisher}...")
    Enum.each urls, fn(url) ->
      message = {:scrape, {url, publisher}}
      :"article_scraper_pool #{publisher}"
      |> :poolboy.transaction(&(GenServer.cast(&1, message)), @pool_timeout)
    end
  end

  defp cooldown(publisher) do
    Logger.info("Cooldown: #{publisher}")
    :timer.sleep(@source_cooldown)
  end
end
