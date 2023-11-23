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



