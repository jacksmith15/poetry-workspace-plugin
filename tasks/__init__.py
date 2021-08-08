from invoke import Collection

from tasks.changelog_check import changelog_check
from tasks.lint import lint
from tasks.release import build, release
from tasks.test import coverage, test
from tasks.typecheck import typecheck
from tasks.verify import verify

namespace = Collection(
    build,
    changelog_check,
    coverage,
    lint,
    release,test,
    typecheck,
    verify,
)
