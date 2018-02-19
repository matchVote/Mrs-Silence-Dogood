use Mix.Config

config :logger, level: System.get_env("LOG_LEVEL")

config :dogood, Dogood.Repo,
  adapter: Ecto.Adapters.Postgres,
  database: System.get_env("DB_NAME"),
  username: System.get_env("DB_USER"),
  password: System.get_env("DB_PASSWORD"),
  hostname: System.get_env("DB_HOST"),
  port: System.get_env("DB_PORT")

config :dogood, kickoff_count: System.get_env("KICKOFF_COUNT")
config :dogood, article_scrapers_per_source: 5
config :dogood, cooldown: 600_000  # 10 minutes
