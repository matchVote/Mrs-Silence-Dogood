defmodule Dogood.Repo.Migrations.AddMentionedCountToArticlesRepresentatives do
  use Ecto.Migration

  def change do
    alter table(:articles_representatives) do
      add :mentioned_count, :integer
    end
  end
end
