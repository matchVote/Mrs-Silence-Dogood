defmodule Test.Dogood.Models.ArticleTest do
  use ExUnit.Case
  alias Dogood.Models.Article

  test "url must not be null" do
    article = %Article{}
    cs = Article.changeset(article, %{})
    refute cs.valid?
  end
end
