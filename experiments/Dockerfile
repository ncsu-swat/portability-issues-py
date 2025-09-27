FROM python:3.12-slim
RUN apt-get update && apt-get install -y git nano cloc htop
COPY . /app

# create venv env
RUN python -m venv /app/env

WORKDIR /app