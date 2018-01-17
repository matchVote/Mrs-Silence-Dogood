defmodule Dogood.ArticleScraper do
  require Logger
  use GenServer

  def start_link(_) do
    GenServer.start_link(__MODULE__, nil)
  end

  def handle_cast({:scrape, {url, publisher}}, nil) do
    scrape(url, publisher)
    {:noreply, nil}
  end

  def scrape(url, publisher) do
    Logger.info("Scraping #{url} for #{publisher}...")
    url
    |> request_article()
    |> Dogood.NLPService.extract_data()
    |> process_article()
  end

  defp request_article(url) do
    %{body: html} = HTTPoison.get!(url)
    html
  end

  def process_article(article) do
    case Dogood.NLPService.classify(article.text) do
      "political" ->
        article
        |> Dogood.NLPService.analyze()
        |> insert()
        |> link_article_to_officials()
      _ -> nil
    end
  end

  def insert(article) do
    Dogood.Repo.insert(article)
  end

  def link_article_to_officials(article) do
    article
  end
end
