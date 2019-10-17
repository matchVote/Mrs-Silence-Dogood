defmodule Dogood.Repo do
  use Ecto.Repo,
    otp_app: :dogood,
    adapter: Ecto.Adapters.Postgres
end
