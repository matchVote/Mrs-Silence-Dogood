defmodule Dogood.ArticleScraper do
  require Logger
  use GenServer
  alias Dogood.Models.Article

  @scraping_timeout 10_000  # 10 seconds

  # Client

  def start_link(_) do
    GenServer.start_link(__MODULE__, nil)
  end

  def scrape_article(scraper, url, publisher) do
    GenServer.call(scraper, {:scrape, {url, publisher}}, @scraping_timeout)
  end

  # Server

  def handle_call({:scrape, {url, publisher}}, _, nil) do
    Logger.info("#{inspect self()} scraping: #{url}")
    scrape(url, publisher)
    {:reply, nil, nil}
  end

  def scrape(url, publisher) do
    url
    |> request_article()
    |> extract_data()
    |> process_article(url, publisher)
  end

  defp request_article(url) do
    %{body: html} = HTTPoison.get!(url, [], recv_timeout: 10_000)
    html
  end

  def process_article(article, url, publisher) do
    case classify(article.text) do
      "political" ->
        article
        |> analyze()
        |> prepare_changeset(url, publisher)
        |> insert()
        |> link_article_to_officials()
      _ -> nil
    end
  end

  def prepare_changeset(article, url, publisher) do
    Article.changeset(article, %{url: url, publisher: publisher})
  end

  def insert(article_changeset) do
    Dogood.Repo.insert(article_changeset)
  end

  def link_article_to_officials(article) do
    article
  end

  defp extract_data(html), do: Dogood.NLP.extract_data(html)
  defp classify(text), do: Dogood.NLP.classify(text)
  defp analyze(article), do: Dogood.NLP.analyze(article)
end
