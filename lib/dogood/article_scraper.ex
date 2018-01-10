defmodule Dogood.ArticleScraper do
  require Logger
  use GenServer
  alias Dogood.Models.Article

  @nlp_service_domain "http://#{System.get_env("NLP_SERVICE")}"

  def scrape(url) do
    Logger.info("Scraping article #{url}...")
    %{body: html} = HTTPoison.get!(url)
    article = parse(html)
    case classify(article.text) do
      "political" ->
        article
        |> IO.inspect
        # |> analyze
        # |> insert
        # |> insert_rep_link
      _ -> nil
    end
  end

  def parse(html) do
    post_data = Poison.encode!(%{html: html})
    @nlp_service_domain <> "/extract"
    |> HTTPoison.post!(post_data)
    |> decode_response_into_article()
  end

  defp decode_response_into_article(%{body: json}) do
    Poison.decode!(json, as: %Article{})
  end

  def classify(text) do
    post_data = Poison.encode!(%{text: text})
    @nlp_service_domain <> "/classify"
    |> HTTPoison.post!(post_data)
    |> decode_classification()
  end

  defp decode_classification(%{body: json}) do
    Poison.decode!(json)["classification"]
  end
end
