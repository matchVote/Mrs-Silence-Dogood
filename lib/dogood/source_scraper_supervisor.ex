defmodule Dogood.SourceScraperSupervisor do
  use Supervisor

  def start_link(source) do
    Supervisor.start_link(__MODULE__, source)
  end

  def init(source) do
    children = [
      {Dogood.ArticleScraperSupervisor, [source["publisher"]]},
      {Dogood.SourceScraper, [source]},
    ]
    Supervisor.init(children, strategy: :one_for_one)
  end
end
