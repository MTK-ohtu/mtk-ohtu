FROM python:3.10-bookworm

WORKDIR /app

RUN pip install poetry

COPY . /app

EXPOSE 5000

ENV FLASK_APP=app.py

RUN poetry install

ENTRYPOINT ["./init_config", "poetry", "run", "flask", "run"]