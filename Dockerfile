FROM python:3.10-bookworm
#FROM python:3.10-alpine

WORKDIR /app

#ENV PATH="/home/appuser/.local/bin:$PATH"

# COPY requirements.txt .
# COPY poetry.lock .
# COPY pyproject.toml .
# COPY ./src/* .

COPY . ./

RUN chmod -R 777 *
#--chown=:root --chmod=770 . ./

# RUN apk update \
#     && apk add libpg-dev

RUN pip install poetry
#RUN curl -sSL https://install.python-poetry.org | python3 -

EXPOSE 5000

RUN poetry config installer.max-workers 10

#RUN poetry add $(cat requirements.txt)

#RUN poetry update
#RUN poetry install --no-interaction --no-ansi -vvv --no-root
RUN poetry install --no-root

#ENTRYPOINT ["poetry", "run", "flask", "--app", "src/app.py", "run", "--host", "0.0.0.0"]
CMD ["/bin/sh"]