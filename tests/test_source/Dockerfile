FROM python:3.6.3

LABEL maintainer="matchVote <admin@matchvote.com>"
LABEL version="0.0.1"

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app
ENV FLASK_APP service.py
