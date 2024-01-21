FROM python:3.10-alpine

WORKDIR /app

COPY . .

RUN pip install poetry

EXPOSE 5000

ENV FLASK_APP=app.py

RUN poetry install

ENTRYPOINT ["/bin/sh", "-c", "chmod +x ./init_config.sh && ./init_config.sh && poetry run flask run --host 0.0.0.0"]