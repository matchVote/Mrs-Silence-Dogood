defmodule Test.Dogood.ArticleScraper do
  use ExUnit.Case, async: true
  import Mock
  alias Dogood.ArticleScraper

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
      article = ArticleScraper.parse("<html>mock article</html>")
      assert article.title == "Article Title"
      assert article.authors == ["Bob Lewis", "Jane Goodall"]
      assert article.text == "Awesome article here"
      assert article.date_published == nil
    end
  end

  test "classify returns 'political' when a known Official is mentioned" do
    text = "You are not Peter King"
    mock_post = fn(_url, _body) ->
      %{body: Poison.encode!(%{classification: "political"})}
    end
    with_mock HTTPoison, [post!: mock_post] do
      assert ArticleScraper.classify(text) == "political"
      expected_url = "http://docker.for.mac.localhost:8000/classify"
      expected_json = Poison.encode!(%{text: text})
      assert called HTTPoison.post!(expected_url, expected_json)
    end
  end
end
