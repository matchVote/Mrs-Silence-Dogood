defmodule Dogood.Models.Article do
  @derive [Poison.Encoder]
  use Ecto.Schema
  import Ecto.Changeset

  schema "articles" do
    field :url, :string
    field :title, :string
    field :authors, {:array, :string}
    field :publisher, :string
    field :date_published, :utc_datetime
    field :keywords, {:array, :string}
    field :summary, :string
    field :read_time, :integer
    field :newsworthiness_count, :integer, default: 0
    field :top_image_url, :string
    field :source, :string
    field :read_count, :integer, default: 0
    field :text, :string, virtual: true
    timestamps()
  end

  def changeset(article, params \\ %{}) do
    article
    |> cast(params, [:title, :date_published])
    |> validate_required([:url, :publisher])
  end
end
