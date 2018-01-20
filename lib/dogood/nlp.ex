defmodule Dogood.NLP do
  require Logger
  alias Dogood.Models.Article

  @nlp_service "http://#{System.get_env("NLP_SERVICE")}"
  @request_timeout 30_000  # 30 seconds

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
    %{body: json} =
      HTTPoison.post!(
        @nlp_service <> resource,
        Poison.encode!(data),
        [],
        recv_timeout: @request_timeout,
        ssl: [versions: :"tlsv1.2"]  # necessary to avoid Erlang bug ERL-192
      )
    json
  end
end
