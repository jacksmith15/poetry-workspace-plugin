import shutil
import subprocess

import pytest

from tests.console.commands.constants import PROJECT_ROOT


@pytest.fixture(autouse=True)
def setup_root_project():
    subprocess.run(["poetry", "new", str(PROJECT_ROOT)], check=True, capture_output=True)
    assert PROJECT_ROOT.exists()
    try:
        yield
    finally:
        shutil.rmtree(PROJECT_ROOT)
