defmodule Dogood.Scraper do
  use GenServer
  require Logger

  def start_link([]) do
    GenServer.start_link(__MODULE__, nil)
  end

  def init(nil) do
    unless System.get_env("CONSOLE") == "true" do
      send(self(), :execute)
    end
    {:ok, nil}
  end

  def handle_info(:execute, nil) do
    execute()
    {:noreply, nil}
  end

  def execute do
    [pub | _] = _publishers = Dogood.Publishers.active_list()
    Logger.info("Extracting articles for #{pub.name}")
    articles = Dogood.Publishers.extract_articles(pub)
    Logger.info("Consuming #{length(articles)} #{pub.name} articles... (mmmmmm yummy)")
    Enum.each(articles, &Dogood.Articles.consume/1)
    Logger.info("Done")

    cooldown()
    execute()
  end

  def cooldown do
    Logger.info("Initiating cooldown...")
    :timer.sleep(Application.get_env(:dogood, :cooldown))
  end
end
