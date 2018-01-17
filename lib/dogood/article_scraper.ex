defmodule Dogood.ArticleScraper do
  require Logger
  use GenServer
  alias Dogood.Models.Article

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
    |> Dogood.NLP.extract_data()
    |> IO.inspect
    |> process_article(url, publisher)
  end

  defp request_article(url) do
    %{body: html} = HTTPoison.get!(url)
    html
  end

  def process_article(article, url, publisher) do
    case Dogood.NLP.classify(article.text) do
      "political" ->
        article
        |> Dogood.NLP.analyze()
        |> add_required_data(url, publisher)
        |> insert()
        |> link_article_to_officials()
      _ -> nil
    end
  end

  def add_required_data(article, url, publisher) do
    Article.changeset(article, %{url: url, publisher: publisher})
  end

  def insert(article_changeset) do
    Dogood.Repo.insert(article_changeset)
  end

  def link_article_to_officials(article) do
    article
  end
end
