defmodule Dogood.Supervisor do
  use Supervisor

  def start_link do
    Supervisor.start_link(__MODULE__, nil)
  end

  def init(_) do
    children = [Dogood.Repo | source_scraper_supervisor_specs()]
    Supervisor.init(children, strategy: :one_for_one)
  end

  def source_scraper_supervisor_specs do
    sources()
    |> Enum.slice(0..1)
    |> Enum.map(fn(source) ->
      supervisor_id = :"source_scraper_supervisor #{source["publisher"]}"
      {Dogood.SourceScraperSupervisor, source}
      |> Supervisor.child_spec(id: supervisor_id)
    end)
  end

  defp sources do
    :code.priv_dir(:dogood)
    |> Path.join("sources.yml")
    |> YamlElixir.read_from_file
    |> Map.get("sources")
  end
end
