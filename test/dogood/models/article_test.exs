defmodule Test.Dogood.Models.ArticleTest do
  @moduledoc """
  Side effect free model tests
  """
  use ExUnit.Case, async: true
  alias Dogood.Models.Article

  @valid_attrs %{url: "http://dot.com", title: "Hey!", publisher: "CNN"}

  test "url must not be null" do
    cs = Article.changeset(%Article{}, Map.put(@valid_attrs, :url, nil))
    refute cs.valid?
  end

  test "publisher must not be null" do
    cs = Article.changeset(%Article{}, Map.put(@valid_attrs, :publisher, nil))
    refute cs.valid?
  end

  test "title must not be null" do
    cs = Article.changeset(%Article{}, Map.put(@valid_attrs, :publisher, nil))
    refute cs.valid?
  end

  test "all validations pass" do
    cs = Article.changeset(%Article{}, @valid_attrs)
    assert cs.valid?
  end
end
