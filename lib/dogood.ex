defmodule Dogood do
  def env, do: Application.get_env(:dogood, :env)
  def console_session?, do: _console_session?()

  defp _console_session?() do
    case System.get_env("CONSOLE") do
      "true" -> true
      _ -> false
    end
  end
end
