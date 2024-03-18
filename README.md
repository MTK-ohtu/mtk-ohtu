# mtk-ohtu [![badge](https://github.com/MTK-ohtu/mtk-ohtu/workflows/CI/badge.svg)](https://github.com/MTK-ohtu/mtk-ohtu/actions)[![codecov](https://codecov.io/gh/MTK-ohtu/mtk-ohtu/graph/badge.svg?token=U4WI4WSGPC)](https://codecov.io/gh/MTK-ohtu/mtk-ohtu)

## About
A logistics optimization tool for connecting biomass sidestream sellers, buyers and logistics providers.

To be used in: https://www.kiertoasuomesta.fi/

Staging environment: https://mtk-ohtu-docker-ohtuprojekti-staging.apps.ocp-test-0.k8s.it.helsinki.fi/

## Setting up

First, clone the project to your computer:
```
git clone git@github.com:MTK-ohtu/mtk-ohtu.git
```
Then install the dependencies and compile the language files:
```
poetry install
poetry run invoke compile-translations
```

### Configuration

To run this app, some enviroment variables need to be set. To do this, find `.env.template` in the project's root folder and rename it to `.env`. The environment variables are default-configured for running with Docker Compose. For running manually, configure the variables inside the file separately.

### Running with Docker Compose

To build and start the **whole** application (add `--detached` if you want to run in detached mode):
```bash
docker compose up --build
```
If you want to start the server yourself with `poetry run invoke start` (see: [Running manually](#running-manually)), but want to start the other containers necessary for local development (also see: [Setting up a local Nominatim server](#setting-up-a-local-nominatim-server)), run the following command:
```
docker compose up postgres nominatim
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

### Setting up a local Nominatim server
To set up a local Nominatim server, some steps need to be taken:
1. Create a folder with the name `nominatim` in the project root directory.
1. Download an OSM PBF map of Finland and save it in the `nominatim` folder with the name `finland.osm.pbf`. An example source: https://download.openstreetmap.fr/extracts/europe/finland.osm.pbf
3. In the `.env` file, change the environment variable `NOMINATIM_DOMAIN` to the proper domain. If you are running the serber manually, set it to `localhost:8080`. If you are running it inside Docker Compose, set it to `nominatim:8080`.

Running the Nominatim server for the first time may take over half an hour. It is therefore recommended that you only run the Nominatim server with Docker Compose thusly:
```
docker compose up nominatim
```

Later, when running the **whole** application with Docker Compose, specify the components separately so that the whole command is:
```
docker compose up app postgres nominatim --build
```

### Running manually

#### Installation

(After the steps mentioned in "Setting up")
1. Set up a PostgreSQL database.
2. Configure enviroment variables. See: [Configuration](#configuration).
3. Start the app with the command: `poetry run invoke start`.

## Translation and localisation
The project uses [Babel](https://python-babel.github.io/flask-babel/) for translations.

The following commands are to be executed in `poetry shell`.

To translate a new piece of text:
1. Replace the text (`X`) with `{{ _("X") }}` (in a Jinja2 template) or `_("X")` (in a Python file; use `from flask_babel import _`)
2. Run `inv update-translations`
3. Change the `.po` files in [src/mtk_ohtu/translations](./src/mtk_ohtu/translations)
4. Run `inv compile-translations`

To initialize a new language:
1. Run `inv init-language --language XXXXX`
2. Change the `.po` files in [src/mtk_ohtu/translations](./src/mtk_ohtu/translations)
3. Run `inv compile-translations`

## Documentation

Main documentation folder: [docs](./docs/)

Definition of done: https://github.com/MTK-ohtu/mtk-ohtu/blob/main/docs/Definition_of_done.md

API documentation: [api.md](./docs/api.md)

## License

## Project progress

Product backlog: https://github.com/orgs/MTK-ohtu/projects/7

## Frameworks & libraries used

