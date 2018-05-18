defmodule Dogood.RedditScraperTest do
  use ExUnit.Case

  test "convert_to_integer takes a string and returns integer" do
    assert Dogood.RedditScraper.convert_to_integer("10.3k") == 10_300
    assert Dogood.RedditScraper.convert_to_integer("1.9k") == 1_900
  end
end
