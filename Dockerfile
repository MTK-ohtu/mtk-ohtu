FROM python:3.10-slim-bookworm

WORKDIR /app

COPY . ./

RUN chmod -R 777 .

RUN pip install poetry

ENV POETRY_VIRTUALENVS_IN_PROJECT=true

EXPOSE 5000

RUN poetry config installer.max-workers 10

RUN poetry install

RUN echo -e '\nBUILD_DATE="'`TZ="Europe/Helsinki" date`\" >> .env

ENTRYPOINT ["poetry", "run", "flask", "--app", "mtk_ohtu.app", "run", "--host", "0.0.0.0"]
