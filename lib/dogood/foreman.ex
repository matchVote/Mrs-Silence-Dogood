defmodule Dogood.Foreman do
  use GenServer
  require Logger
  alias Dogood.ScrapingSupervisor

  # Client

  def start_link(_) do
    GenServer.start_link(__MODULE__, nil, name: __MODULE__)
  end

  def publisher_finished(publisher) do
    GenServer.cast(__MODULE__, {:done, publisher})
  end

  # Server

  def init(_) do
    send(self(), :kickoff)
    {:ok, sources()}
  end

  def handle_info(:kickoff, sources) do
    count = kickoff_count()
    kickoff(sources, count)
    {:noreply, Enum.slice(sources, count..-1)}
  end

  def handle_cast({:done, _publisher}, []) do
    Logger.info "All sources done; initiating cooldown..."
    cooldown()
    send(self(), :kickoff)
    {:noreply, sources()}
  end
  def handle_cast({:done, publisher}, [source | sources]) do
    Logger.info "Finished scraping #{publisher}"
    Dogood.ScrapingSupervisor.start_child(publisher_child_spec(source))
    {:noreply, sources}
  end

  defp kickoff(_, 0), do: nil
  defp kickoff(sources, count) do
    IO.puts "Kicking off #{count} sources."
    sources
    |> Enum.slice(0..count-1)
    |> Enum.each(&ScrapingSupervisor.start_child(publisher_child_spec(&1)))
  end

  defp kickoff_count() do
    to_integer(Application.get_env(:dogood, :kickoff_count))
  end

  defp to_integer(value) when is_binary(value), do: String.to_integer(value)
  defp to_integer(value) when is_integer(value), do: value

  defp publisher_child_spec(source) do
    {Dogood.PublisherScraperSupervisor, source}
  end

  defp sources do
    :code.priv_dir(:dogood)
    |> Path.join("sources.yml")
    |> YamlElixir.read_from_file
    |> Map.get("sources")
  end

  defp cooldown, do: :timer.sleep(Application.get_env(:dogood, :cooldown))
end
