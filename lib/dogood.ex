defmodule Dogood do
  def env, do: Application.get_env(:dogood, :env)
end
