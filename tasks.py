from invoke import task

@task
def create(ctx):
    ctx.run("psql -f ./db/setup.sql")

@task
def seed(ctx):
    ctx.run("python seed.py")

@task
def test(ctx):
    ctx.run("pytest")

@task
def playground(ctx):
    ctx.run("psql -f playground.sql > playground.txt")

@task
def secret(ctx):
    ctx.run("python JWT.py")

@task
def production(ctx):
    ctx.run("export FLASK_ENV=production")

@task
def development(ctx):
    ctx.run("export FLASK_ENV=development")