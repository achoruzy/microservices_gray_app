# syntax=docker/dockerfile:1

FROM python:3.9.5-slim-buster

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./app .

