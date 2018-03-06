defmodule Dogood.Publishers do
  alias Dogood.Models.Publisher

  def active_list do
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
end
