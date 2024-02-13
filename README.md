# mtk-ohtu ![badge](https://github.com/MTK-ohtu/mtk-ohtu/workflows/CI/badge.svg)[![codecov](https://codecov.io/gh/MTK-ohtu/mtk-ohtu/graph/badge.svg?token=U4WI4WSGPC)](https://codecov.io/gh/MTK-ohtu/mtk-ohtu)

## About
A logistics optimization tool for connecting biomass sidestream sellers, buyers and logistics providers.

To be used in: https://www.kiertoasuomesta.fi/

## Setting up

### Configuration

To run this app, enviroment variable need to be set. To do this, find `.env.template` on projects root folder and rename it to `.env`.
Next, you need to generate a secret key. You can do this for example with command: `python3 -c 'import secrets; print(secrets.token_hex())'`. Replace PUT_THE_KEY_HERE with the generated secret key inside .env -file.

### Running with Docker Compose

**To build and start** the application (add `--detached` if you want to run in detached mode):
```bash
docker compose up --build
```
**To shut the application down**, first exit the process (Ctrl+C) and then run:
```
docker compose down
```
Docker Compose will create a database folder `postgresql-data` in the project directory to store the PostgreSQL database. To delete and reset the database, simply delete the `postgresql-data` directory.

To create mock data for the database, run the following commands after starting the application:
```
docker exec -it mtk-postgres bash
psql -U postgres < db_mock_data.sql
```


### Running manually

#### Installation

1. Clone the project to your computer.
2. Install dependencies with command: `poetry install`.
3. Configure enviroment variables. See "Configuration".
4. Start the app with command: `poetry run invoke start`.


## Documentation

Definition of done: https://github.com/MTK-ohtu/mtk-ohtu/blob/main/docs/Definition_of_done.md

## License

## Project progress

Product backlog: https://github.com/orgs/MTK-ohtu/projects/7

App: _link here_


## Frameworks & libraries used

