defmodule Dogood.ArticleScraper do
  require Logger
  use GenServer
  alias Dogood.Models.{Article, ArticleOfficial}

  @scraping_timeout 20_000  # 20 seconds

  # Client

  def start_link(_) do
    GenServer.start_link(__MODULE__, nil)
  end

  def scrape_article(scraper, url, publisher) do
    GenServer.call(scraper, {:scrape, {url, publisher}}, @scraping_timeout)
  end

  # Server

  def handle_call({:scrape, {url, publisher}}, _, nil) do
    scrape(url, publisher)
    {:reply, nil, nil}
  end

  def scrape(url, publisher) do
    url
    |> request_article()
    |> extract_data()
    |> process_article(url, publisher)
  end

  def request_article(url) do
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
    article
    |> Article.changeset(%{
      url: url,
      publisher: publisher,
      date_published: normalize_date(article.date_published)
    })
  end

  def normalize_date(nil), do: DateTime.utc_now()
  def normalize_date(_), do: nil

  def insert(article_changeset) do
    case Dogood.Repo.insert(article_changeset) do
      {:ok, article} ->
        Logger.info("Inserted #{article.publisher} article - ID: #{article.id}")
        article
      {:error, _} -> nil
    end
  end

  def link_article_to_officials(nil), do: nil
  def link_article_to_officials(article) do
    article.mentioned_officials_ids
    |> Enum.each(fn(official_id) ->
      %ArticleOfficial{article_id: article.id, representative_id: official_id}
      |> Dogood.Repo.insert()
    end)
  end

  defp extract_data(html), do: Dogood.NLP.extract_data(html)
  defp classify(text), do: Dogood.NLP.classify(text)
  defp analyze(article), do: Dogood.NLP.analyze(article)
end
