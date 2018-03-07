defmodule Dogood.Publishers do
  alias Dogood.Models.{Article, Publisher}

  def active_list do
    read_publishers_from_file()
  end

  defp read_publishers_from_file do
    publishers_file()
    |> YamlElixir.read_from_file()
    |> Map.get("publishers")
    |> Enum.sort()
    |> Enum.map(&%Publisher{name: &1["name"], url: &1["url"]})
  end

  defp publishers_file do
    case Mix.env do
      :test -> "test/support/publishers.yml"
      _ -> Path.join(:code.priv_dir(:dogood), "publishers.yml")
    end
  end

  def extract_articles(%Publisher{} = publisher) do
    publisher.url
    |> parse_publisher()
    |> filter_urls()
    |> create_articles(publisher.name)
  end

  def parse_publisher(url) do
    case Dogood.NLP.parse_publisher(url) do
      {:ok, urls} -> urls
      _ -> nil
    end
  end

  def filter_urls(nil), do: []

  def filter_urls(urls) do
    urls
    |> Enum.uniq()
    |> Enum.filter(&String.ends_with?(&1, ".html"))
  end

  def create_articles([], _), do: []

  def create_articles(urls, publisher) do
    for url <- urls, do: %Article{url: url, publisher: publisher}
  end
end
