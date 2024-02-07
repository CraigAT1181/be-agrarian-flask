from invoke import task

@task
def create(ctx):
    ctx.run("psql -f ./db/setup.sql")

@task
def dseed(ctx):
    ctx.run("python dev_seed.py")

@task
def pseed(ctx):
    ctx.run("python prod_seed.py")

@task
def test(ctx):
    ctx.run("pytest")

@task
def playground(ctx):
    ctx.run("psql -f playground.sql > playground.txt")

@task
def secret(ctx):
    ctx.run("python JWT.py")
