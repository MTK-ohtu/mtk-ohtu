FROM python:3.10-alpine

RUN adduser -D -G root appuser

WORKDIR /app

ENV PATH="/home/appuser/.local/bin:$PATH"

COPY . ./

RUN chown -R :0 /app && \
    chmod -R g=u /app

USER appuser

RUN pip install poetry
#RUN curl -sSL https://install.python-poetry.org | python3 -

RUN which poetry

EXPOSE 5000

RUN poetry install --no-root

ENTRYPOINT ["/bin/sh", "-c", "poetry run flask --app src/app run --host 0.0.0.0"]