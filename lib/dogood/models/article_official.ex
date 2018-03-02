defmodule Dogood.Models.ArticleOfficial do
  use Ecto.Schema

  schema "articles_representatives" do
    field(:representative_id, :binary_id)
    timestamps(inserted_at: :created_at)
    belongs_to(:article, Dogood.Models.Article)
  end
end
