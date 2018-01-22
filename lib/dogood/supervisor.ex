defmodule Dogood.Supervisor do
  use Supervisor

  def start_link do
    Supervisor.start_link(__MODULE__, nil)
  end

  def init(_) do
    count = System.get_env("SOURCES")
    children = [Dogood.Repo | source_scraper_supervisor_specs(count)]
    Supervisor.init(children, strategy: :one_for_one)
  end

  def source_scraper_supervisor_specs("0"), do: []
  def source_scraper_supervisor_specs(nil) do
    sources()
    |> Enum.slice(0..5)
    |> Enum.map(fn(source) ->
      {Dogood.SourceScraperSupervisor, source}
      |> Supervisor.child_spec(id: supervisor_id(source))
    end)
  end

  defp sources do
    :code.priv_dir(:dogood)
    |> Path.join("sources.yml")
    |> YamlElixir.read_from_file
    |> Map.get("sources")
  end

  defp supervisor_id(%{"publisher" => publisher}) do
    publisher = String.replace(publisher, " ", "")
    :"source_scraper_supervisor-#{publisher}"
  end
end
