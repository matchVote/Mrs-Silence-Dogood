defmodule Dogood.HTTP do
  def get(url) do
    HTTPoison.get!(url, [], recv_timeout: 10_000).body
  end

  def post(url, data) do
    options = [
      recv_timeout: 30_000,  # 30 seconds
      ssl: [versions: :"tlsv1.2"]  # necessary to avoid Erlang bug ERL-192
    ]
    HTTPoison.post!(url, Poison.encode!(Map.new(data)), [], options).body
  end
end
