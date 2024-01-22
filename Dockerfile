FROM python:3.10-alpine

WORKDIR /app

COPY . .

RUN pip install poetry

EXPOSE 5000

RUN poetry install

ENTRYPOINT ["/bin/sh", "-c", "src/init_config.sh && poetry run flask --app src/app run --host 0.0.0.0"]