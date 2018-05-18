defmodule Dogood.PublishersTest do
  use ExUnit.Case
  alias Dogood.Publishers

  setup do
    urls = [
      "https://link1.com",
      "/",
      "/resource/topic",
      "http://www.hey.org/what",
      "http://www.hey.org/actual/article.html"
    ]

    %{urls: urls}
  end

  test "active_list/0 returns a list of sorted publishers" do
    [publisher | _] = publishers = Publishers.active_list()
    assert 3 == length(publishers)
    assert "http://anywhere.com" == publisher.url
    assert "Anywhere" == publisher.name
    assert ["Anywhere", "Nowhere", "Somewhere"] == Enum.map(publishers, & &1.name)
  end

  test "filter_urls/1 only keeps urls ending in .html", %{urls: urls} do
    expected = ["http://www.hey.org/actual/article.html"]
    results = Publishers.filter_urls(urls)
    assert expected == results
  end

  test "filter_urls/1 removes duplicate urls" do
    urls = [
      "http://www.hey.org/actual/article.html",
      "http://www.hey.org/actual/article.html"
    ]

    expected = ["http://www.hey.org/actual/article.html"]
    results = Publishers.filter_urls(urls)
    assert expected == results
  end
end
