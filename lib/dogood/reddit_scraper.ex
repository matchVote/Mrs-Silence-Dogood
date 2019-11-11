defmodule Dogood.RedditScraper do
  use GenServer
  require Logger

  @url "https://www.reddit.com/r/politics/"
  @publisher "Reddit Politics"

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
    article_count =
      Dogood.HTTP.get(@url)
      |> extract_article_urls_and_votes()
      |> Enum.map(&create_article/1)
      |> Enum.map(fn article ->
        Task.start(__MODULE__, :consume, [article])
      end)
      |> length

    Logger.info("Reddit Scraper article count #{article_count}")
    :timer.sleep(Application.get_env(:dogood, :reddit_cooldown))
    execute()
  end

  def extract_article_urls_and_votes(html) do
    Floki.find(html, ".Post")
    |> Enum.filter(fn post -> Floki.find(post, "article") != [] end)
    |> Enum.map(fn post -> {extract_url(post), extract_vote(post)} end)
  end

  defp extract_url(post) do
    Floki.find(post, "article a")
    |> Floki.attribute("href")
    |> Enum.uniq()
    |> Enum.filter(fn url ->
      String.contains?(url, "http") &&
        !String.contains?(url, "www.reddit.com/r/politics/comments")
    end)
    |> List.first()
  end

  defp extract_vote(post) do
    Floki.find(post, "button + div")
    |> List.first()
    |> elem(2)
    |> List.first()
    |> convert_to_integer()
  end

  def convert_to_integer(vote) do
    Regex.replace(~r/[.k]/, vote, "")
    |> String.replace("•", "0")
    |> String.to_integer()
  end

  defp create_article({url, votes}) do
    %Dogood.Models.Article{
      url: url,
      publisher: @publisher,
      newsworthiness_count: votes
    }
  end

  def consume(article) do
    article
    |> Dogood.Articles.download()
    |> Dogood.Articles.parse()
    |> Dogood.Articles.classify()
    |> Dogood.Articles.analyze()
    |> change_date_published()
    |> Dogood.Articles.persist()
  end

  def change_date_published(nil), do: nil

  def change_date_published(article) do
    Map.put(article, :date_published, DateTime.utc_now())
  end
end
