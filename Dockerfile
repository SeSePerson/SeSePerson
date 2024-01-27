FROM tiangolo/uvicorn-gunicorn:python3.10-slim

LABEL authors="coming"

WORKDIR /app

ENV PATH="${PATH}:/root/.local/bin"

ADD . /app/

EXPOSE 8788

RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN /usr/local/bin/python -m pip install  --no-cache-dir --upgrade --quiet pip

RUN poetry install

VOLUME /app/accounts /app/data

CMD poetry run python3 main.py
