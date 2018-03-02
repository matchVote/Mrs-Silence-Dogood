defmodule Dogood.HTTP do
  def get(url) do
    HTTPoison.get!(url, [], recv_timeout: 10_000).body
  end

  def post(url, data) do
    options = [
      # 30 seconds
      recv_timeout: 30_000,
      # necessary to avoid Erlang bug ERL-192
      ssl: [versions: :"tlsv1.2"]
    ]

    json = Poison.encode!(Map.new(data))

    case HTTPoison.post(url, json, [], options) do
      {:error, %HTTPoison.Error{reason: reason}} -> {:error, reason} 
      response -> response
    end
  end
end
