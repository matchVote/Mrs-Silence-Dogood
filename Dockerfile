FROM elixir:1.6.1

RUN mix local.hex --force && \
    mix local.rebar --force

WORKDIR /usr/src/app
COPY . .

RUN rm -rf deps/* && \
    mix deps.get

CMD ["elixir", "-S", "mix", "run", "--no-halt"]
