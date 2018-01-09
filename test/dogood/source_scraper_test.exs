defmodule SourceScraperTest do
  use ExUnit.Case

  test "it does something" do
    source = %{url: "http://cnn.com", publisher: "CNN"}
    Dogood.SourceScraper.scrape(source)
  end
end
