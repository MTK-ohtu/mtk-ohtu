from invoke import task

@task
def start(ctx):
    ctx.run('flask run', pty = True)

@task
def test(ctx):
    ctx.run("coverage run --branch -m pytest src", pty=True)
    ctx.run("coverage html", pty=True)

@task
def lint(ctx):
    ctx.run("pylint src", pty=True)