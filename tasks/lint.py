from invoke import task
from termcolor import cprint

from tasks.helpers import package, print_header


@task()
def lint(ctx):
    """Run linter on source code and tests.

    A non-zero return code from this task indicates invalid code was discovered.
    """
    print_header("RUNNING LINTER")

    ctx.run(f"pyflakes {package.__name__} tasks tests", pty=True)
    # pyflakes doesn't give positive output
    cprint("✔ No issues found.", "green")
