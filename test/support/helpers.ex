defmodule Dogood.Test.Helpers do
  @moduledoc """
  Various functions to aid in testing
  """

  def insert_article(attrs) do
    %Dogood.Models.Article{}
    |> Map.merge(attrs)
    |> Dogood.Repo.insert()
  end
end
