defmodule Test.Dogood.ArticleScraperTest do
  use Dogood.Test.DBCase, async: true
  import Mock
  alias Dogood.ArticleScraper
  alias Dogood.Models.Article
  alias Dogood.NLP

  setup do
    mocked_functions = [
      classify: fn(_) -> "political" end,
      analyze: fn(article) ->
        Map.put(article, :mentioned_officials_ids, generate_uuids(4))
      end
    ]
    %{mocked_functions: mocked_functions}
  end

  test "process_article saves article to database if it's classified as political", setup do
    process_article_with_mocked_functions(setup.mocked_functions)
    article = Repo.one(from a in Article, where: a.title == "test")
    assert article.url == "http://dot.com"
  end

  test "process_article creates a link between article and mentioned officials", setup do
    process_article_with_mocked_functions(setup.mocked_functions)
    query = from a in Article,
            where: a.title == "test",
            preload: [:linked_officials]
    article = Repo.one(query)
    assert length(article.linked_officials) == 4
  end

  test "prepare_changeset creates a changeset with given data" do
    article = %Article{title: "something"}
    changeset = ArticleScraper.prepare_changeset(article, "url", "publisher")
    assert "url" == get_change(changeset, :url)
    assert "publisher" == get_change(changeset, :publisher)
  end

  defp process_article_with_mocked_functions(mocked_functions) do
    with_mock NLP, mocked_functions do
      %Article{url: "http://dot.com", title: "test", publisher: "XYZ"}
      |> ArticleScraper.process_article("http://dot.com", "test")
    end
  end

  defp generate_uuids(num) do
    for _ <- 1..num, do: Ecto.UUID.generate()
  end
end
