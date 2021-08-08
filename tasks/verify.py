from invoke import task

from tasks.changelog_check import changelog_check
from tasks.lint import lint
from tasks.test import test
from tasks.typecheck import typecheck


@task(post=[changelog_check, lint, typecheck, test])
def verify(_ctx):
    """Run all verification steps."""
