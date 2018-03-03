defmodule Dogood.NLP do
  require Logger
  alias Dogood.Models.Article

  def parse_source(source_url) do
    case request("/parse_source", %{url: source_url}) do
      {:ok, response} ->
        {:ok, decode(response.body)["article_urls"]}

      {:error, reason} ->
        Logger.warn("NLP/parse_source failed: #{reason} -- #{source_url}")
    end
  end

  def extract_data(html) do
    case request("/extract", %{html: html}) do
      {:ok, response} -> decode(response.body, as: %Article{})
      {:error, reason} -> Logger.warn("NLP/extract failed: #{reason}")
    end
  end

  def classify(text) do
    case request("/classify", %{text: text}) do
      {:ok, response} -> decode(response.body)["classification"]
      {:error, reason} -> Logger.warn("NLP/classify failed: #{reason}")
    end
  end

  def analyze(article) do
    case request("/analyze", %{text: article.text, title: article.title}) do
      {:ok, response} -> struct(article, decode(response.body, keys: :atoms))
      {:error, reason} -> Logger.warn("NLP/analyze failed: #{reason}")
    end
  end

  defp request(resource, data) do
    Dogood.HTTP.post(service_url(resource), data)
  end

  defp decode(json, options \\ []) do
    case Poison.decode(json, options) do
      {:ok, map} -> map
      {:error, _} -> Logger.warn("FAILED -- JSON decoding: #{json}")
    end
  end

  defp service_url(resource) do
    host = Application.get_env(:dogood, :nlp_service_host)
    port = Application.get_env(:dogood, :nlp_service_port)
    "#{host}:#{port}#{resource}"
  end
end
