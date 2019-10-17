use Mix.Config

config :logger, level: System.get_env("LOG_LEVEL") || :warn

config :dogood, env: :prod

config :dogood, Dogood.Repo,
  adapter: Ecto.Adapters.Postgres,
  database: System.get_env("DB_NAME"),
  username: System.get_env("DB_USER"),
  password: System.get_env("DB_PASSWORD"),
  hostname: System.get_env("DB_HOST"),
  port: System.get_env("DB_PORT")

config :dogood, nlp_service_host: System.get_env("NLP_SERVICE_HOST")
config :dogood, nlp_service_port: System.get_env("NLP_SERVICE_PORT")
config :dogood, max_consumers: System.get_env("MAX_CONSUMERS") || 20
# 10 minutes
config :dogood, cooldown: 600_000
# 1 hour
config :dogood, reddit_cooldown: 3_600_000
