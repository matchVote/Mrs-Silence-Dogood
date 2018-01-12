defmodule Test.Dogood.Models.ArticleRepoTest do
  @moduledoc """
  Test database side effects of Article model
  """

  use Dogood.Test.DBCase
  alias Dogood.Models.Article

  @valid_attrs %{url: "http://dot.com", title: "Hey!", publisher: "CNN"}

  test "url must be unique" do
    insert_article(@valid_attrs)
    new_attrs = %{url: "http://dot.com", title: "Yo", publisher: "ABC"}
    changeset = Article.changeset(%Article{}, new_attrs)

    assert {:error, changeset} = Repo.insert(changeset)
    {error, _} = changeset.errors[:url]
    assert error == "has already been taken"
  end

  test "title must be unique" do
    insert_article(@valid_attrs)
    new_attrs = %{url: "http://bar.com", title: "Hey!", publisher: "ABC"}
    changeset = Article.changeset(%Article{}, new_attrs)

    assert {:error, changeset} = Repo.insert(changeset)
    {error, _} = changeset.errors[:title]
    assert error == "has already been taken"
  end
end
