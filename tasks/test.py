import re
import webbrowser
from pathlib import Path

from invoke import task

from tasks.helpers import package, print_header

_COVERAGE_PATH = Path("reports/cover")


@task(optional=["debug", "maxfail"])
def test(ctx, debug=False, maxfail=0):
    """Run tests.

    A non-zero return code from this task indicates some tests failed.
    """
    print_header("RUNNING TESTS")
    flags = [
        "--verbose",
        f"--cov={package.__name__}",
        "--cov-branch",
        f'--cov-report="html:{_COVERAGE_PATH}"',
    ]
    if debug:
        flags.append("--capture=no")
    if maxfail:
        flags.append(f"--maxfail={int(maxfail)}")

    ctx.run(f"pytest {' '.join(flags)} tests/", pty=True)
    print(f"\nCoverage: {get_total_coverage(ctx)}")


@task
def coverage(ctx):
    """Open browsable coverage report."""
    path = (_COVERAGE_PATH / "index.html").absolute()
    webbrowser.open(f"file:///{path}")


def get_total_coverage(ctx) -> str:
    """Return coverage percentage, as captured in coverage dat file.

    :return: string percentage coverage, e.g. "100%".
    """
    output = ctx.run(
        "coverage report",
        hide=True,
    ).stdout
    match = re.search(r"TOTAL.*?([\d.]+%)", output)
    if match is None:
        raise RuntimeError(f"Regex failed on output: {output}")
    return match.group(1)
