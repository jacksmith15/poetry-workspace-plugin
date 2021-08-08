from invoke import task

from tasks.helpers import package, print_header


@task()
def typecheck(ctx):
    """Run type checking on source code and tests.

    A non-zero return code from this task indicates invalid types were discovered.
    """
    print_header("RUNNING TYPE CHECKER")

    ctx.run(f"mypy {package.__name__} tasks tests", pty=True)
