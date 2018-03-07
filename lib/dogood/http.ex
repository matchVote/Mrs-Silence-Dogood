defmodule Dogood.HTTP do
  require Logger

  @get_options [
    connect_timeout: 10_000,
    recv_timeout: 10_000,
    follow_redirect: true
  ]

  @post_options [
    connect_timeout: 10_000,
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
    with {:ok, json} <- encode_json(data),
         {:ok, %HTTPoison.Response{status_code: 200}} = response <-
           HTTPoison.post(url, json, [], @post_options) do
      response
    else
      {:error, %HTTPoison.Error{reason: reason}} ->
        {:error, reason}

      {:error, _} = error ->
        error
    end
  end

  defp encode_json(data) do
    try do
      Poison.encode(Map.new(data))
    rescue
      FunctionClauseError -> {:error, :binary_not_encodable}
    end
  end
end
