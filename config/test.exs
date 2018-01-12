use Mix.Config

config :dogood, Dogood.Repo,
  adapter: Ecto.Adapters.Postgres,
  database: "dogood_test",
  username: "postgres",
  password: "postgres",
  hostname: "postgres",
  pool: Ecto.Adapters.SQL.Sandbox
