defmodule Dogood.PublishersTest do
  use ExUnit.Case
  alias Dogood.Publishers

  test "active_list/0 returns a list of publishers" do
    [publisher | _] = publishers = Publishers.active_list()
    assert 3 == length(publishers)
    assert "http://somewhere.com" == publisher.url
    assert "Somewhere" == publisher.name
  end
end
