from invoke import task
from termcolor import cprint

from tasks.helpers import print_header


@task()
def changelog_check(ctx):
    """Run validator on changelog.

    A non-zero return code from this task indicates invalid changelog was discovered.
    """
    print_header("RUNNING CHANGELOG VALIDATOR")

    ctx.run("changelog validate", pty=True)
    # changelog doesn't give positive output
    cprint("✔ No issues found.", "green")
