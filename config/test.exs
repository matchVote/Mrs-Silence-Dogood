use Mix.Config

config :logger, level: :warn

config :dogood, env: :test

config :dogood, Dogood.Repo,
  adapter: Ecto.Adapters.Postgres,
  database: "matchvote_test",
  username: "postgres",
  password: "postgres",
  hostname: "localhost",
  port: 5653,
  pool: Ecto.Adapters.SQL.Sandbox

config :dogood, kickoff_count: 0
