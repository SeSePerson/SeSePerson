FROM tiangolo/uvicorn-gunicorn:python3.10-slim

LABEL authors="coming"

WORKDIR /app

ENV PATH="${PATH}:/root/.local/bin"

ADD . /app/

EXPOSE 8788

RUN sed -i "s@http://deb.debian.org@http://mirrors.aliyun.com@g" /etc/apt/sources.list && rm -Rf /var/lib/apt/lists/* && apt-get update

RUN apt install curl -y

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN /usr/local/bin/python -m pip install  --no-cache-dir --upgrade --quiet pip

RUN poetry install

VOLUME /app/accounts /app/data

CMD poetry run python3 main.py