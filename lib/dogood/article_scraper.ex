defmodule Dogood.ArticleScraper do
  require Logger
  alias Dogood.Models.{Article, ArticleOfficial}

  def scrape(url, publisher) do
    url
    |> request_article()
    |> extract_data()
    |> process_article(url, publisher)
  end

  def request_article(url), do: Dogood.HTTP.get(url)

  defp extract_data(nil), do: nil
  defp extract_data(html), do: Dogood.NLP.extract_data(html)

  def process_article(%Article{} = article, url, publisher) do
    case classify(article.text) do
      "political" ->
        article
        |> analyze()
        |> prepare_changeset(url, publisher)
        |> insert()
        |> link_article_to_officials()

      _ ->
        nil
    end
  end

  def process_article(_, _, _), do: nil

  def prepare_changeset(article, url, publisher) do
    new_fields = %{
      url: url,
      publisher: publisher,
      date_published: normalize_date(article.date_published)
    }

    Article.changeset(article, new_fields)
  end

  def normalize_date(nil), do: DateTime.utc_now()
  def normalize_date(_), do: nil

  def insert(article_changeset) do
    case Dogood.Repo.insert(article_changeset) do
      {:ok, article} ->
        Logger.info("Inserted #{article.publisher} article - ID: #{article.id}")
        article

      {:error, _} ->
        nil
    end
  end

  def link_article_to_officials(nil), do: nil

  def link_article_to_officials(article) do
    article.mentioned_officials_ids
    |> Enum.each(fn official_id ->
      %ArticleOfficial{article_id: article.id, representative_id: official_id}
      |> Dogood.Repo.insert()
    end)
  end

  defp classify(text), do: Dogood.NLP.classify(text)
  defp analyze(article), do: Dogood.NLP.analyze(article)
end
