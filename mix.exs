defmodule Dogood.Mixfile do
  use Mix.Project

  def project do
    [
      app: :dogood,
      version: "0.1.0",
      elixir: "~> 1.5",
      start_permanent: Mix.env == :prod,
      deps: deps()
    ]
  end

  def application do
    [
      extra_applications: [:logger],
      # mod: {Dogood.Application, []}
    ]
  end

  defp deps() do
    [
      {:ecto, "2.2.0"},
      {:httpoison, "0.13.0"},
      {:poison, "3.1.0"},
      {:postgrex, "0.13.3"},
      {:mock, "0.3.1", only: :test},
    ]
  end
end
