# mtk-ohtu ![badge](https://github.com/MTK-ohtu/mtk-ohtu/workflows/CI/badge.svg)[![codecov](https://codecov.io/gh/MTK-ohtu/mtk-ohtu/graph/badge.svg?token=U4WI4WSGPC)](https://codecov.io/gh/MTK-ohtu/mtk-ohtu)

## About
A logistics optimization tool for connecting biomass sidestream sellers, buyers and logistics providers.

To be used in: https://www.kiertoasuomesta.fi/

## Setting up

First, clone the project to your computer:
```
git clone git@github.com:MTK-ohtu/mtk-ohtu.git
```

### Configuration

To run this app, some enviroment variables need to be set. To do this, find `.env.template` in the project's root folder and rename it to `.env`. The environment variables are default-configured for running with Docker Compose. For running manually, configure the variables inside the file separately.

Regardless of the method of execution, you need to generate a secret key. You can do this with the command: `python3 -c 'import secrets; print(secrets.token_hex())'`. Replace PUT_THE_KEY_HERE in the .env file with the generated secret key.

### Running with Docker Compose

To build and start the **whole** application (add `--detached` if you want to run in detached mode):
```bash
docker compose up --build
```
If you want to start the server yourself with `poetry run invoke start` (see: [Running manually](#running-manually)), but want to start the other containers necessary for local development, run the following command:
```
docker compose up postgres
```
To shut the application down, first exit the process (Ctrl+C) and then run:
```
docker compose down
```
<hr>
Docker Compose will create a database folder `postgresql-data` in the project directory to store the PostgreSQL database. To delete and reset the database, simply delete the `postgresql-data` directory.

To create mock data for the database, run the following commands after starting the application:
```
docker exec -it mtk-postgres bash
psql -U postgres < db_mock_data.sql
```
<hr>


### Running manually

#### Installation

1. Install dependencies with the command: `poetry install`.
2. Set up a PostgreSQL database.
3. Configure enviroment variables. See: [Configuration](#configuration).
4. Start the app with the command: `poetry run invoke start`.

## Documentation

Definition of done: https://github.com/MTK-ohtu/mtk-ohtu/blob/main/docs/Definition_of_done.md

## License

## Project progress

Product backlog: https://github.com/orgs/MTK-ohtu/projects/7

App: _link here_


## Frameworks & libraries used

