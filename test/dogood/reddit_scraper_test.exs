defmodule Dogood.RedditScraperTest do
  use ExUnit.Case

  test "convert_to_integer takes a string and returns integer" do
    assert Dogood.RedditScraper.convert_to_integer("10.3k") == 103
    assert Dogood.RedditScraper.convert_to_integer("1.9k") == 19
  end

  test "convert_to_integer converts bullet point to zero" do
    assert Dogood.RedditScraper.convert_to_integer("•") == 0
  end
end
