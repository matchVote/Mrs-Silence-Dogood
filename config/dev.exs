use Mix.Config

config :dogood, env: :dev

config :dogood, Dogood.Repo,
  adapter: Ecto.Adapters.Postgres,
  database: "dogood_dev",
  username: "postgres",
  password: "postgres",
  hostname: "postgres",
  port: 5432

config :dogood, nlp_service_host: System.get_env("NLP_SERVICE_HOST")
config :dogood, nlp_service_port: System.get_env("NLP_SERVICE_PORT")
config :dogood, max_consumers: System.get_env("MAX_CONSUMERS")
config :dogood, cooldown: 60_000  # 1 minute
