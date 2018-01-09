defmodule Test.Dogood.ArticleScraper do
  use ExUnit.Case
  import Mock

  test "parse returns an Article populated with basic data" do
    extracted_data = %{
      title: "Article Title",
      authors: ["Bob Lewis", "Jane Goodall"],
      text: "Awesome article here",
      date_published: nil,
    }
    mock_post = fn(_url, _body) ->
      %{body: Poison.encode!(extracted_data)}
    end

    with_mock HTTPoison, [post!: mock_post] do
      article = Dogood.ArticleScraper.parse("<html>mock article</html>")
      assert article.title == "Article Title"
      assert article.authors == ["Bob Lewis", "Jane Goodall"]
      assert article.text == "Awesome article here"
      assert article.date_published == nil
    end
  end
end
