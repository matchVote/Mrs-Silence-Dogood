defmodule Dogood.Mixfile do
  use Mix.Project

  def project do
    [
      app: :dogood,
      version: "0.2.0",
      elixir: "~> 1.6",
      elixirc_paths: elixirc_paths(Mix.env),
      start_permanent: Mix.env == :prod,
      deps: deps()
    ]
  end

  def application do
    [
      extra_applications: [:logger],
      mod: {Dogood.Application, []}
    ]
  end

  defp elixirc_paths(:test), do: ["lib", "test/support"]
  defp elixirc_paths(_), do: ["lib"]

  defp deps() do
    [
      {:distillery, "1.5.2", runtime: false},
      {:ecto, "2.2.0"},
      {:floki, "0.19.2"},
      {:httpoison, "0.13.0"},
      {:poison, "3.1.0"},
      {:postgrex, "0.13.3"},
      {:mock, "0.3.1", only: :test},
      {:yaml_elixir, "1.3.0"},
    ]
  end
end
