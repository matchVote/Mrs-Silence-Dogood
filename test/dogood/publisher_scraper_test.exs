defmodule Test.Dogood.PublisherScraperTest do
  use ExUnit.Case
  alias Dogood.PublisherScraper

  setup do
    html = """
    <html>
      <body>
        <a href="https://link1.com">Link1</a>
        <a href="http://www.hey.org/what">what</a>
        <a href="http://www.hey.org/what/article.html">A great article</a>
        <a href="/nothing">Nothing</a>
        <a href="/some/article.html">Another article</a>
      </body>
    </html>
    """

    urls = [
      "https://link1.com",
      "/",
      "/resource/topic",
      "http://www.hey.org/what",
      "http://www.hey.org/actual/article.html",
    ]
    %{html: html, urls: urls}
  end

  test "filter_urls only keeps urls ending in .html", %{urls: urls} do
    expected = ["http://www.hey.org/actual/article.html"]
    results = PublisherScraper.filter_urls(urls)
    assert expected == results
  end

  test "filter_urls removes duplicate urls" do
    urls = [
      "http://www.hey.org/actual/article.html",
      "http://www.hey.org/actual/article.html",
    ]
    expected = ["http://www.hey.org/actual/article.html"]
    results = PublisherScraper.filter_urls(urls)
    assert expected == results
  end
end
