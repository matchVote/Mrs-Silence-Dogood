defmodule Dogood.Repo.Migrations.CreateArticles do
  use Ecto.Migration

  def change do
    create table(:articles) do
      add :url, :text, null: false
      add :title, :text, null: false
      add :publisher, :text, null: false
      add :authors, {:array, :text}
      add :date_published, :utc_datetime
      add :keywords, {:array, :text}
      add :summary, :text
      add :read_time, :integer
      add :top_image_url, :text
      add :source, :text
      timestamps(inserted_at: :created_at)
    end

    create unique_index(:articles, [:url])
    create unique_index(:articles, [:title])
  end
end
