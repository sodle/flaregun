FROM python:3.8.9
RUN pip install poetry

COPY . /app
WORKDIR /app

RUN poetry install
ENTRYPOINT poetry run python main.py --zone=$ZONE --record=$RECORD
