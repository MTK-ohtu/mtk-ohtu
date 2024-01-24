FROM python:3.10-alpine

RUN adduser -D appuser

WORKDIR /app

COPY . .

USER appuser

RUN pip install poetry

EXPOSE 5000

RUN poetry install

ENTRYPOINT ["/bin/sh", "-c", "poetry run flask --app src/app run --host 0.0.0.0"]