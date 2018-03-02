defmodule Dogood.HTTP do
  @get_options [
    recv_timeout: 10_000,
    connect_timeout: 10_000,
    follow_redirect: true
  ]

  @post_options [
    recv_timeout: 30_000,
    # necessary to avoid Erlang bug ERL-192
    ssl: [versions: :"tlsv1.2"]
  ]

  def get(url) do
    case HTTPoison.get(url, [], @get_options) do
      {:ok, response} -> response.body
      _ -> nil
    end
  end

  def post(url, data) do
    json = Poison.encode!(Map.new(data))

    case HTTPoison.post(url, json, [], @post_options) do
      {:error, %HTTPoison.Error{reason: reason}} -> {:error, reason}
      response -> response
    end
  end
end
