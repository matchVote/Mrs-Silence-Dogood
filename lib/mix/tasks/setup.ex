defmodule Mix.Tasks.Db.Setup do
  use Mix.Task

  @shortdoc "Creates and migrates the database"
  def run(args) do
    if "--reset" in args, do: drop_database()
    create_database()
    migrate()
  end

  defp create_database do
    try do
      Mix.Task.run("ecto.create")
    rescue
      _ -> create_database()
    end
  end

  defp migrate do
    Mix.Task.run("ecto.migrate")
  end

  defp drop_database do
    Mix.Task.run("ecto.drop")
  end
end
