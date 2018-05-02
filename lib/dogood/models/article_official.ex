defmodule Dogood.Models.ArticleOfficial do
  use Ecto.Schema

  schema "articles_representatives" do
    field(:representative_id, :binary_id)
    field(:mentioned_count, :integer)
    timestamps(inserted_at: :created_at)
    belongs_to(:article, Dogood.Models.Article)
  end
end
