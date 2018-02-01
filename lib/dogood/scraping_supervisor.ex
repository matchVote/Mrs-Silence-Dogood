defmodule Dogood.ScrapingSupervisor do
  use DynamicSupervisor

  def start_link(_) do
    DynamicSupervisor.start_link(__MODULE__, nil, name: __MODULE__)
  end

  def start_child(spec) do
    DynamicSupervisor.start_child(__MODULE__, spec)
  end

  def init(nil) do
    DynamicSupervisor.init(strategy: :one_for_one)
  end
end
