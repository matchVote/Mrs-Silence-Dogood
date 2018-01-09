defmodule Dogood.Supervisor do
  use Supervisor

  def start_link do
    sources = []
    Supervisor.start_link(__MODULE__, sources)
  end

  def init(_sources) do
    children = [Dogood.Repo]
    Supervisor.init(children, strategy: :one_for_one)
  end
end
