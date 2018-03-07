use Mix.Config

config :dogood, Dogood.Repo,
  adapter: Ecto.Adapters.Postgres,
  database: "dogood_dev",
  username: "postgres",
  password: "postgres",
  hostname: "postgres",
  port: 5432

config :dogood, nlp_service_host: System.get_env("NLP_SERVICE_HOST")
config :dogood, nlp_service_port: System.get_env("NLP_SERVICE_PORT")
config :dogood, cooldown: 15_000  # 15 seconds
