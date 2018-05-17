defmodule Dogood.RedditScraper do
  use GenServer
  require Logger

  @url "https://www.reddit.com/r/politics/"
  @publisher "Reddit Politics"
  # 1 hour
  @cooldown 3_600_000

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
    Logger.info("Kicking off Reddit Scraper.")
    execute()
    {:noreply, nil}
  end

  def execute do
    articles =
      Dogood.HTTP.get(@url)
      |> extract_article_urls_and_votes()

    Logger.info("Reddit Scraper article count #{length(articles)}")
    cooldown()
    execute()
  end

  def extract_article_urls_and_votes(html) do
    Floki.find(html, ".Post")
    |> Enum.filter(fn post -> Floki.find(post, "article") != [] end)
    |> Enum.map(fn post -> {extract_url(post), extract_vote(post)} end)
  end

  def extract_url(post) do
    Floki.find(post, "article a")
    |> Floki.attribute("href")
    |> Enum.uniq
    |> Enum.filter(fn url ->
      String.contains?(url, "http") &&
        !String.contains?(url, "www.reddit.com/r/politics/comments") 
    end)
    |> List.first
  end

  def extract_vote(post) do
    Floki.find(post, "button + div")
    |> List.first
    |> elem(2)
    |> List.first
  end

  def consume(article) do
    Logger.info("Reddit article! #{article.url}")
    # article
    # |> download()
    # |> parse()
    # |> classify()
    # |> analyze()
    # |> reddit_stuff()
  end

  def cooldown do
    Logger.info("Reddit Scraper taking a break!")
    :timer.sleep(@cooldown)
  end
end
