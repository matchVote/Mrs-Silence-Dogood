defmodule Test.Dogood.ArticleScraper do
  use Dogood.Test.DBCase, async: true
  import Mock
  alias Dogood.ArticleScraper
  alias Dogood.Models.Article
  alias Dogood.NLPService

  test "process_article saves article to database if it's classified as political" do
    mocked_functions = [
      classify: fn(_) -> "political" end,
      analyze: fn(article) -> article end
    ]
    with_mock NLPService, mocked_functions do
      %Article{url: "http://dot.com", title: "test", publisher: "XYZ"}
      |> ArticleScraper.process_article()
    end

    article = Repo.one(from a in Article, where: a.title == "test")
    assert article.url == "http://dot.com"
  end

  @tag :skip
  test "process_article creates a link between article and mentioned officials" do
  end
end
