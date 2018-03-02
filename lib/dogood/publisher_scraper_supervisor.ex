defmodule Dogood.PublisherScraperSupervisor do
  use Supervisor

  def start_link(source) do
    Supervisor.start_link(__MODULE__, source)
  end

  def init(source) do
    children = [
      {Task.Supervisor, name: supervisor_name(source["publisher"])},
      {Dogood.PublisherScraper, source}
    ]

    Supervisor.init(children, strategy: :one_for_one)
  end

  defp supervisor_name(publisher) do
    :"article_scraper_supervisor-#{publisher}"
  end
end
