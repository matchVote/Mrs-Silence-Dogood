defmodule Dogood.Articles do
  require Logger
  alias Dogood.Models.Article

  @spec consume(%Article{}) :: any
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

  def classify(%Article{} = article) do
    {Dogood.NLP.classify(article.text), article}
  end

  def classify(_), do: nil

  def analyze({"political", %Article{} = article}) do
    Dogood.NLP.analyze(article)
  end

  def analyze(_), do: nil

  def persist(nil), do: nil

  def persist(article) do
    article
    |> prepare_changeset()
    |> insert()
  end

  def prepare_changeset(nil), do: nil

  def prepare_changeset(article) do
    new_fields = %{
      date_published: Dogood.Utils.normalize_date(article.date_published)
    }

    Article.changeset(article, new_fields)
  end

  def insert(article_changeset) do
    case Dogood.Repo.insert(article_changeset) do
      {:ok, article} ->
        Logger.info("Inserted #{article.publisher} article - ID: #{article.id}")
        article

      {:error, _} ->
        nil
    end
  end
end
