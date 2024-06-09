FROM python:3.11.1-slim

WORKDIR /word_card

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install -r requirements.txt