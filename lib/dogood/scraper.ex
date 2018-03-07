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
    scrape_publishers(Dogood.Publishers.active_list())
    cooldown()
    execute()
  end

  def scrape_publishers([publisher | remaining_publishers]) do
    Logger.info("#{publisher.name}: Extracting articles")
    articles = Dogood.Publishers.extract_articles(publisher)
    Logger.info("#{publisher.name}: Consuming #{length(articles)} articles")
    Enum.each(articles, &Dogood.Articles.consume/1)
    Logger.info("#{publisher.name}: Scraping complete")
    scrape_publishers(remaining_publishers)
  end

  def scrape_publishers([]), do: nil

  def cooldown do
    Logger.info("Initiating cooldown...")
    :timer.sleep(Application.get_env(:dogood, :cooldown))
  end
end
