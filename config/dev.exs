use Mix.Config

config :logger, level: :info

config :dogood, Dogood.Repo,
  adapter: Ecto.Adapters.Postgres,
  database: "dogood_dev",
  username: "postgres",
  password: "postgres",
  hostname: "postgres",
  port: 5432

config :dogood, kickoff_count: 3
config :dogood, article_scrapers_per_source: 5
config :dogood, cooldown: 600_000  # 10 minutes
