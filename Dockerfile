FROM python:3.10-bookworm

WORKDIR /app

RUN pip install poetry

COPY . /app

EXPOSE 8080

RUN poetry install

ENTRYPOINT ["poetry", "run", "python", "-m", "src/index.py"]