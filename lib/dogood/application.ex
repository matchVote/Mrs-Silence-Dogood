defmodule Dogood.Application do
  use Application

  def start(_type, _args) do
    Dogood.Supervisor.start_link()
  end
end
