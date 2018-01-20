defmodule Dogood.ArticleScraperSupervisor do
  use Supervisor

  def start_link(publisher) do
    Supervisor.start_link(__MODULE__, publisher)
  end

  def init(publisher) do
    pool_name = :"article_scraper_pool-#{publisher}"
    children = [
      :poolboy.child_spec(pool_name, poolboy_config(pool_name))
    ]
    Supervisor.init(children, strategy: :one_for_one)
  end

  defp poolboy_config(pool_name) do
    [
      {:name, {:local, pool_name}},
      {:worker_module, Dogood.ArticleScraper},
      {:size, 5},
      {:max_overflow, 0},
    ]
  end
end
