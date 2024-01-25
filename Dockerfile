FROM python:3.10-alpine

WORKDIR /app

#ENV PATH="/home/appuser/.local/bin:$PATH"

COPY . . 

RUN chmod -R 777 *
#--chown=:root --chmod=770 . ./

RUN pip install poetry
#RUN curl -sSL https://install.python-poetry.org | python3 -

EXPOSE 5000

RUN poetry config installer.max-workers 10

RUN poetry add $(cat requirements.txt)

RUN poetry install --no-interaction --no-ansi -vvv --no-root
#RUN poetry install --no-root

ENTRYPOINT ["poetry run flask --app src/app run --host 0.0.0.0"]