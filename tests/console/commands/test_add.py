import os
import subprocess

import pytest

from tests.console.commands.helpers import PROJECT_ROOT, run


class TestWorkspaceAdd:
    @staticmethod
    def should_add_new_workspace_from_given_path():
        # GIVEN a poetry project exists at a given path
        workspace_relpath = "libs/my-library"
        # workspace_path = PROJECT_ROOT / workspace_relpath
        run(["poetry", "new", workspace_relpath])
        # WHEN I add the path as a workspace
        run(["poetry", "workspace", "add", workspace_relpath])
        # THEN the project should now be tracked as a workspace in the root project
        assert run(["poetry", "workspace", "list"]).text == "my-library libs/my-library"

    @staticmethod
    def should_fail_when_project_with_that_name_already_exists():
        # GIVEN a project is already tracked
        run(["poetry", "workspace", "new", "libs/my-library"])
        # AND another project exists with the same name
        run(["poetry", "new", "other/my-library"])
        # WHEN I attempt to add that project as a workspace
        with pytest.raises(subprocess.CalledProcessError) as exc_info:
            run(["poetry", "workspace", "add", "other/my-library"])
        exc = exc_info.value
        # THEN the exit code is 1
        assert exc.returncode == 1
        # AND the expected error message is displayed
        assert exc.text == "Workspace already registered with name my-library"

    @staticmethod
    def should_fail_when_target_path_doesnt_exist():
        # WHEN I attempt to add a workspace from a path which does not exist
        with pytest.raises(subprocess.CalledProcessError) as exc_info:
            run(["poetry", "workspace", "add", "libs/my-library"])
        exc = exc_info.value
        # THEN the exit code is 1
        assert exc.returncode == 1
        # AND the expected error message is displayed
        assert "Path 'libs/my-library' does not exist." in exc.text

    @staticmethod
    def should_fail_when_pyproject_is_not_present():
        # GIVEN a directory exists but does not contain a pyproject.toml
        path = "libs/my-library"
        os.makedirs(PROJECT_ROOT / path)
        # WHEN I attempt to add that path as a workspace
        with pytest.raises(subprocess.CalledProcessError) as exc_info:
            run(["poetry", "workspace", "add", "libs/my-library"])
        exc = exc_info.value
        # THEN the exit code is 1
        assert exc.returncode == 1
        # AND the expected error message is displayed
        assert f"Poetry could not find a pyproject.toml file in {path!r}." in exc.text

    @staticmethod
    def should_fail_when_not_a_poetry_project():
        # GIVEN a directory contains an empty pyproject.toml
        path = "libs/my-library"
        os.makedirs(PROJECT_ROOT / path)
        (PROJECT_ROOT / path / "pyproject.toml").touch()
        # WHEN I attempt to add that path as a workspace
        with pytest.raises(subprocess.CalledProcessError) as exc_info:
            run(["poetry", "workspace", "add", "libs/my-library"])
        exc = exc_info.value
        # THEN the exit code is 1
        assert exc.returncode == 1
        # AND the expected error message is displayed
        assert f"The Poetry configuration at {str(path)!r} is invalid:" in exc.text, exc.text
