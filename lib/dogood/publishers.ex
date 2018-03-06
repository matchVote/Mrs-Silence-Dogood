defmodule Dogood.Publishers do
  alias Dogood.Models.Publisher

  def active_list do
    read_publishers_from_file()
  end

  defp read_publishers_from_file do
    publishers_file()
    |> YamlElixir.read_from_file()
    |> Map.get("publishers")
    |> Enum.map(&%Publisher{name: &1["name"], url: &1["url"]})
  end

  defp publishers_file do
    case Mix.env do
      :test -> "test/support/publishers.yml"
      _ -> Path.join(:code.priv_dir(:dogood), "publishers.yml")
    end
  end

  def extract_article_urls(%Publisher{url: url}) do
    url
    |> parse_publisher()
    |> filter_urls()
  end

  def parse_publisher(url) do
    case Dogood.NLP.parse_publisher(url) do
      {:ok, urls} -> urls
      _ -> nil
    end
  end

  def filter_urls(nil), do: nil

  def filter_urls(urls) do
    urls
    |> Enum.uniq()
    |> Enum.filter(&String.ends_with?(&1, ".html"))
  end
end
