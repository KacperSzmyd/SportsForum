FROM python:3.8

ENV PYTHONBUFFERED=1

WORKDIR /code

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt