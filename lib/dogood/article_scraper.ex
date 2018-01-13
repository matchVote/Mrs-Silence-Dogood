defmodule Dogood.ArticleScraper do
  require Logger
  use GenServer

  def scrape(url) do
    Logger.info("Scraping article #{url}...")
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
        # |> insert_official_link()
      _ -> nil
    end
  end

  def insert(article) do
    Dogood.Repo.insert(article)
  end
end
