defmodule SourceScraperTest do
  use ExUnit.Case
  alias Dogood.SourceScraper

  setup do
    html = """
    <html>
      <body>
        <a href="https://link1.com">Link1</a>
        <a href="http://www.hey.org/what">A great article</a>
      </body>
    </html>
    """
    %{html: html}
  end

  test "extract_anchor_urls returns a list of urls from html", %{html: html} do
    urls = SourceScraper.extract_anchor_urls(html)
    assert urls == [
      "https://link1.com",
      "http://www.hey.org/what",
    ]
  end
end
