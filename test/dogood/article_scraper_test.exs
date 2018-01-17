defmodule Test.Dogood.ArticleScraper do
  use Dogood.Test.DBCase, async: true
  import Mock
  alias Dogood.ArticleScraper
  alias Dogood.Models.Article
  alias Dogood.NLP

  test "process_article saves article to database if it's classified as political" do
    mocked_functions = [
      classify: fn(_) -> "political" end,
      analyze: fn(article) -> article end
    ]
    with_mock NLP, mocked_functions do
      %Article{url: "http://dot.com", title: "test", publisher: "XYZ"}
      |> ArticleScraper.process_article("http://dot.com", "test")
    end

    article = Repo.one(from a in Article, where: a.title == "test")
    assert article.url == "http://dot.com"
  end

  @tag :skip
  test "process_article creates a link between article and mentioned officials" do
  end

  test "add_required_data creates a changeset with given data" do
    article = %Article{title: "something"}
    changeset = ArticleScraper.add_required_data(article, "url", "publisher")
    assert "url" == get_change(changeset, :url)
    assert "publisher" == get_change(changeset, :publisher)
  end
end
