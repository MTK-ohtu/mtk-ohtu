FROM python:3.10-bookworm

WORKDIR /app

RUN pip install poetry

COPY . /app

EXPOSE 8080

ENV FLASK_APP=app.py

RUN poetry install

ENTRYPOINT ["poetry", "run", "flask", "run"]