defmodule Dogood.Utils do
  require Logger

  def normalize_date(nil), do: DateTime.utc_now()

  def normalize_date(value) do
    case convert_unix_seconds_to_datetime(value) do
      {:ok, datetime} -> datetime
      :error -> value
    end
  end

  defp convert_unix_seconds_to_datetime(value) do
    case convert_value_to_integer(value) do
      {:ok, seconds} ->
        convert_seconds_to_datetime(seconds)

      :not_convertible ->
        :error
    end
  end

  defp convert_seconds_to_datetime(seconds) do
    case DateTime.from_unix(seconds) do
      {:ok, datetime} ->
        log_conversion_success(seconds, datetime)
        {:ok, datetime}

      {:error, reason} ->
        log_conversion_error(seconds, reason)
        {:ok, normalize_date(nil)}
    end
  end

  defp convert_value_to_integer(value) when is_integer(value), do: {:ok, value}

  defp convert_value_to_integer(value) when is_binary(value) do
    try do
      {:ok, String.to_integer(value)}
    rescue
      ArgumentError -> :not_convertible
    end
  end

  defp log_conversion_success(seconds, datetime) do
    Logger.info("Unix seconds (#{seconds}) converted to DateTime: #{inspect(datetime)}")
  end

  defp log_conversion_error(seconds, reason) do
    Logger.info("Error converting unix seconds to DateTime: #{seconds} -- #{reason}")
  end
end
