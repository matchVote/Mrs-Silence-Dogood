use Mix.Config

config :logger, level: :warn

config :dogood, env: :test

config :dogood, Dogood.Repo,
  adapter: Ecto.Adapters.Postgres,
  database: "dogood_test",
  username: "postgres",
  password: "postgres",
  hostname: "postgres",
  port: 5432,
  pool: Ecto.Adapters.SQL.Sandbox

config :dogood, kickoff_count: 0
