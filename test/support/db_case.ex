defmodule Dogood.Test.DBCase do
  use ExUnit.CaseTemplate

  using do
    quote do
      alias Dogood.Repo
      import Dogood.Test.Helpers
      import Ecto.Query
      import Ecto.Changeset
    end
  end

  setup tags do
    :ok = Ecto.Adapters.SQL.Sandbox.checkout(Dogood.Repo)

    unless tags[:async] do
      Ecto.Adapters.SQL.Sandbox.mode(Dogood.Repo, {:shared, self()})
    end

    :ok
  end
end
