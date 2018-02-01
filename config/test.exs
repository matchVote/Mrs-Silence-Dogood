use Mix.Config

config :logger, level: :warn

config :dogood, Dogood.Repo,
  adapter: Ecto.Adapters.Postgres,
  database: "dogood_test",
  username: "postgres",
  password: "postgres",
  hostname: "postgres",
  pool: Ecto.Adapters.SQL.Sandbox

config :dogood, kickoff_count: 0
