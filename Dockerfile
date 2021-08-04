# syntax=docker/dockerfile:1

FROM python:3.9.5-slim-buster

COPY ./app /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

EXPOSE 8080

COPY ./requirements.txt requirements.txt
COPY ./setup.py setup.py
RUN pip3 install -r requirements.txt
RUN pip install -e .

WORKDIR /app