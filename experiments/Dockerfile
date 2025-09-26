FROM python:3.12-slim
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY . /app

# create venv env
RUN python -m venv /app/env

WORKDIR /app