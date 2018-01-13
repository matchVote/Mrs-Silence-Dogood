defmodule Dogood.NLPService do
  alias Dogood.Models.Article
  
  @nlp_service_domain "http://#{System.get_env("NLP_SERVICE")}"

  def extract_data(html) do
    "#{@nlp_service_domain}/extract"
    |> HTTPoison.post!(Poison.encode!(%{html: html}))
    |> Poison.decode!(as: %Article{})
  end

  def classify(text) do
    %{body: json} = "#{@nlp_service_domain}/classify"
    |> HTTPoison.post!(Poison.encode!(%{text: text}))
    Poison.decode!(json)["classification"]
  end

  def analyze(article) do
    article
  end
end
