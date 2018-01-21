defmodule Dogood.Repo.Migrations.CreateArticlesRepresentatives do
  use Ecto.Migration

  def change do
    create table(:articles_representatives) do
      add :article_id, :id, null: false
      add :representative_id, :binary_id, null: false
      timestamps(inserted_at: :created_at)
    end

    create unique_index(
      :articles_representatives,
      [:article_id, :representative_id]
    )
  end
end
