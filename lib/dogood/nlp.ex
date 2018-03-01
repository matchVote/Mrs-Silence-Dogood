defmodule Dogood.NLP do
  require Logger
  alias Dogood.Models.Article

  def parse_source(source_url) do
    json = request("/parse_source", %{url: source_url})
    Poison.decode!(json)["article_urls"]
  end

  def extract_data(html) do
    json = request("/extract", %{html: html})
    Poison.decode!(json, as: %Article{})
  end

  def classify(text) do
    json = request("/classify", %{text: text})
    Poison.decode!(json)["classification"]
  end

  def analyze(article) do
    json = request("/analyze", %{text: article.text, title: article.title})
    data = Poison.decode!(json, keys: :atoms)
    struct(article, data)
  end

  defp request(resource, data) do
    service_url(resource)
    |> Dogood.HTTP.post(data)
  end

  defp service_url(resource) do
    host = Application.get_env(:dogood, :nlp_service_host)
    port = Application.get_env(:dogood, :nlp_service_port)
    "#{host}:#{port}#{resource}"
  end
end
