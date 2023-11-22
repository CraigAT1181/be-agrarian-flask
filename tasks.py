from invoke import task

@task
def playground(ctx):
    ctx.run("psql -f playground.sql > playground.txt")

@task
def test(ctx):
    ctx.run("pytest")

