# Starts all dependencies of dogood without starting dogood itself
# Used in conjunction with `mix test --no-start`
Application.load(:dogood)

for app <- Application.spec(:dogood, :applications) do
  Application.ensure_all_started(app)
end

ExUnit.start()
Dogood.Repo.start_link()
Ecto.Adapters.SQL.Sandbox.mode(Dogood.Repo, :manual)
