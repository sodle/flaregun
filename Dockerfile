FROM python:3.8.9

COPY . /app
RUN pip install poetry

WORKDIR /app
RUN poetry install
ENTRYPOINT poetry run python main.py --zone=$ZONE --record=$RECORD
