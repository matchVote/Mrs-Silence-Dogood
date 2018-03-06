defmodule Dogood.Articles do
  require Logger
  alias Dogood.Models.{Article, ArticleOfficial}

  def consume(article) do
    article
    |> download()
    |> parse()
    |> classify()
    |> analyze()
    |> persist()
  end

  def download(article) do
    %{article | html: Dogood.HTTP.get(article.url)}
  end

  def parse(%Article{html: nil}), do: nil

  def parse(article) do
    Dogood.NLP.parse_article(article)
  end

  def classify(nil), do: nil

  def classify(%Article{} = article) do
    {Dogood.NLP.classify(article.text), article}
  end

  def analyze(nil), do: nil

  def analyze({classification, %Article{} = article}) do
    Dogood.NLP.analyze(article)
  end

  def persist(nil), do: nil

  def persist(article) do
    article
    |> prepare_changeset()
    |> insert()
    |> link_to_officials()
  end

  def prepare_changeset(nil), do: nil

  def prepare_changeset(article) do
    new_fields = %{
      date_published: normalize_date(article.date_published)
    }

    Article.changeset(article, new_fields)
  end

  def normalize_date(nil), do: DateTime.utc_now()
  def normalize_date(date), do: date

  def insert(article_changeset) do
    case Dogood.Repo.insert(article_changeset) do
      {:ok, article} ->
        Logger.info("Inserted #{article.publisher} article - ID: #{article.id}")
        article

      {:error, _} ->
        nil
    end
  end

  def link_to_officials(nil), do: nil

  def link_to_officials(article) do
    article.mentioned_officials_ids
    |> Enum.each(fn official_id ->
      %ArticleOfficial{article_id: article.id, representative_id: official_id}
      |> Dogood.Repo.insert()
    end)
  end
end
