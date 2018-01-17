defmodule Dogood.NLP do
  alias Dogood.Models.Article

  @nlp_service_domain "http://#{System.get_env("NLP_SERVICE")}"

  def extract_data(html) do
    json = request("/extract", %{html: html})
    Poison.decode!(json, as: %Article{})
  end

  def classify(text) do
    json = request("/classify", %{text: text})
    Poison.decode!(json)["classification"]
  end

  def analyze(article) do
    article
  end

  defp request(resource, data) do
    %{body: json} =
      @nlp_service_domain <> resource
      |> HTTPoison.post!(Poison.encode!(data))
    json
  end
end
