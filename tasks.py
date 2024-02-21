from invoke import task
from dotenv import load_dotenv

load_dotenv()

@task
def start(ctx):
    ctx.run('flask --app mtk_ohtu.app run', pty = True)

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

@task
def mockstart(ctx):
    reset_db(ctx)
    fill_mock(ctx)
    start(ctx)


@task
def test(ctx):
    ctx.run("coverage run --branch -m pytest src", pty=True)
    ctx.run("coverage html", pty=True)

@task
def lint(ctx):
    ctx.run("pylint src", pty=True)