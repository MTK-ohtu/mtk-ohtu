# mtk-ohtu ![badge](https://github.com/MTK-ohtu/mtk-ohtu/workflows/CI/badge.svg)[![codecov](https://codecov.io/gh/MTK-ohtu/mtk-ohtu/graph/badge.svg?token=U4WI4WSGPC)](https://codecov.io/gh/MTK-ohtu/mtk-ohtu)

## About
A logistics optimization tool for connecting biomass sidestream sellers, buyers and logistics providers.

To be used in: https://www.kiertoasuomesta.fi/

## Getting started

### Prerequisites

### Installation

1. Clone the project to your computer.
2. Install dependencies with command: `poetry install`.
3. Configure enviroment variables. See "Configuration".
4. Start the app with command: `poetry run invoke start`.

### Run with Docker

1. Build docker image
```bash
docker build -t mtk-ohtu .
```
2. Run container (single use)
```bash
docker run -d -p 5000:5000 --rm mtk-ohtu
```
3. Access app from your web browser in address localhost:5000

You need to build image only once unless you have removed the builded image.


## Configuration

To run this app, enviroment variable need to be set. To do this, find `.env.template` on projects root folder and rename it to `.env`.
Next, you need to generate a secret key. You can do this for example with command: `python3 -c 'import secrets; print(secrets.token_hex())'`. Replace PUT_THE_KEY_HERE with the generated secret key inside .env -file.


## Documentation

Definition of done: https://github.com/MTK-ohtu/mtk-ohtu/blob/main/docs/Definition_of_done.md

## License

## Project progress

Product backlog: https://github.com/orgs/MTK-ohtu/projects/7

App: _link here_


## Frameworks & libraries used

