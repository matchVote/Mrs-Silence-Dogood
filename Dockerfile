FROM elixir:1.6.0

RUN apt-get update \
    && curl -sL https://deb.nodesource.com/setup_6.x | bash - \
    && apt-get install -y -q \
      nodejs \
      inotify-tools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mix local.hex --force \
    && mix local.rebar --force

WORKDIR /usr/src/app

COPY . .
RUN mix deps.get
RUN mix deps.compile

CMD ["bin/start"]
