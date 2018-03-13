use Mix.Config

config :dogood, env: :prod

config :dogood, Dogood.Repo,
  adapter: Ecto.Adapters.Postgres,
  database: "${DB_NAME}",
  username: "${DB_USER}",
  password: "${DB_PASSWORD}",
  hostname: "${DB_HOST}",
  port: "${DB_PORT}"

config :dogood, nlp_service_host: "${NLP_SERVICE_HOST}"
config :dogood, nlp_service_port: "${NLP_SERVICE_PORT}"
config :dogood, max_consumers: "${MAX_CONSUMERS}"
config :dogood, cooldown: 600_000  # 10 minutes
