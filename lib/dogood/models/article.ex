defmodule Dogood.Models.Article do
  @derive [Poison.Encoder]
  use Ecto.Schema
  import Ecto.Changeset

  schema "articles" do
    field :url, :string
    field :title, :string
    field :date_published, :utc_datetime
    field :text, :string, virtual: true
    field :authors, {:array, :string}
    timestamps()
  end

  def changeset(article, params \\ %{}) do
    article
    |> cast(params, [:title, :date_published])
  end
end
