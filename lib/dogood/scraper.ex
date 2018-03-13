defmodule Dogood.Scraper do
  use GenServer
  require Logger

  def start_link([]) do
    GenServer.start_link(__MODULE__, nil)
  end

  def init(nil) do
    unless Dogood.console_session?() do
      send(self(), :execute)
    end

    {:ok, nil}
  end

  def handle_info(:execute, nil) do
    execute()
    {:noreply, nil}
  end

  def execute do
    Dogood.Publishers.active_list()
    |> scrape_publishers()

    cooldown()
    execute()
  end

  def scrape_publishers([publisher | remaining_publishers]) do
    Logger.info("#{publisher.name}: Extracting articles")

    Dogood.Publishers.extract_articles(publisher)
    |> consume_articles(publisher)

    Logger.info("#{publisher.name}: Scraping complete")
    scrape_publishers(remaining_publishers)
  end

  def scrape_publishers([]), do: nil

  def consume_articles(articles, publisher) do
    Logger.info("#{publisher.name}: Consuming #{length(articles)} articles")

    Task.Supervisor.async_stream_nolink(
      Dogood.ConsumerSupervisor,
      articles,
      &Dogood.Articles.consume/1,
      max_concurrency: max_concurrency(),
      timeout: 10_000,
      on_timeout: :kill_task
    )
    |> Enum.to_list()
  end

  defp max_concurrency do
    Application.get_env(:dogood, :max_consumers)
    |> String.to_integer()
  end

  def cooldown do
    Logger.info("Initiating cooldown...")
    :timer.sleep(Application.get_env(:dogood, :cooldown))
  end
end
