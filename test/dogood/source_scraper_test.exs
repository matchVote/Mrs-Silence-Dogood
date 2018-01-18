defmodule SourceScraperTest do
  use ExUnit.Case
  alias Dogood.SourceScraper

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

  test "compile_urls returns all acceptable article urls from html", %{html: html} do
    expected = [
      "http://www.hey.org/what/article.html",
      "http://hey.net/some/article.html",
    ]
    urls = SourceScraper.compile_urls(html, "http://hey.net")
    assert expected == urls
  end

  test "extract_anchor_urls returns a list of urls from html", %{html: html} do
    urls = SourceScraper.extract_anchor_urls(html)
    assert urls == [
      "https://link1.com",
      "http://www.hey.org/what",
      "http://www.hey.org/what/article.html",
      "/nothing",
      "/some/article.html"
    ]
  end

  test "add_prefix adds source domain to beginning of relative url" do
    prefix = "http://www.awesome.com/politics.html"
    urls = ["/some/resource", "http://absolute.com/url"]
    expected = ["http://www.awesome.com/some/resource", "http://absolute.com/url"]
    assert expected == SourceScraper.add_prefix(urls, prefix)
  end

  test "filter_urls only keeps urls ending in .html", %{urls: urls} do
    expected = ["http://www.hey.org/actual/article.html"]
    results = SourceScraper.filter_urls(urls)
    assert expected == results
  end

  test "filter_urls removes duplicate urls" do
    urls = [
      "http://www.hey.org/actual/article.html",
      "http://www.hey.org/actual/article.html",
    ]
    expected = ["http://www.hey.org/actual/article.html"]
    results = SourceScraper.filter_urls(urls)
    assert expected == results
  end
end
