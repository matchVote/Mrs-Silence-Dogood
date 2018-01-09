defmodule Dogood.ArticleScraper do
  require Logger
  use GenServer
  alias Dogood.Models.Article

  def scrape(url) do
    # Logger.info("Scraping article #{url}...")
    # %{body: html} = HTTPoison.get!(url)
    # article = parse(html)  # /extract html
    # case classify(article.text) do
    #   "political" ->
    #     article
    #     |> analyze
    #     |> insert
    #     |> insert_rep_link
    #   _ -> nil
    # end
  end

  def parse(html) do
    post_data = Poison.encode!(%{html: html})
    data =
      nlp_extract_url()
      |> HTTPoison.post!(post_data)
      |> decode_json_into_article()
  end

  defp nlp_extract_url do
    "http://#{System.get_env("NLP_SERVICE")}/extract"
  end

  defp decode_json_into_article(%{body: json}) do
    Poison.decode!(json, as: %Article{})
  end
end
