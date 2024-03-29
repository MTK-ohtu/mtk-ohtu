import secrets
from invoke import task
from dotenv import load_dotenv
import os

load_dotenv()

@task(optional=["debug", "host"])
def start(ctx, debug=False, host="127.0.0.1"):
    ctx.run(f'export SECRET_KEY={secrets.token_hex()}; flask --app mtk_ohtu.app run {"--debug" if debug else ""} --host {host}',
            pty = True)

@task(optional=["workers", "host"])
def production_start(ctx, workers=2, host="127.0.0.1"):
    ctx.run(f"export SECRET_KEY={secrets.token_hex()}; gunicorn -w {workers} -b {host} 'mtk_ohtu.app:app'",
            pty = True)

@task
def reset_db(ctx):
    from mtk_ohtu.config import DATABASE_CONFIG
    from mtk_ohtu.database.db_meta import db_create, db_drop_all

    db_create(DATABASE_CONFIG)
    db_drop_all(DATABASE_CONFIG)
    db_create(DATABASE_CONFIG)

    print("Database reset")


@task
def fill_mock(ctx):
    from mtk_ohtu.config import DATABASE_CONFIG
    from mtk_ohtu.database.db_meta import db_excecute_file

    db_excecute_file("db_mock_data.sql", DATABASE_CONFIG)
    print("Added mock data")

@task(optional=["debug"])
def mockstart(ctx, debug=False):
    reset_db(ctx)
    fill_mock(ctx)
    start(ctx, debug)


@task
def test(ctx):
    ctx.run(f"export SECRET_KEY={secrets.token_hex()}; coverage run --branch -m pytest src", pty=True)
    ctx.run("coverage html", pty=True)

@task
def lint(ctx):
    ctx.run("pylint src", pty=True)

@task
def mockdata(ctx):
    reset_db(ctx)
    fill_mock(ctx)

def extract_translations(ctx):
    ctx.run("pybabel extract -F babel.cfg -o messages.pot .")

def remove_temp_translations():
    os.remove("messages.pot")

@task
def init_language(ctx, language):
    extract_translations(ctx)
    ctx.run(f"pybabel init -i messages.pot -d src/mtk_ohtu/translations -l {language}")
    remove_temp_translations()

@task
def update_translations(ctx):
    extract_translations(ctx)
    ctx.run("pybabel update -i messages.pot -d src/mtk_ohtu/translations")
    remove_temp_translations()

@task
def compile_translations(ctx):
    ctx.run("pybabel compile -f -d src/mtk_ohtu/translations")