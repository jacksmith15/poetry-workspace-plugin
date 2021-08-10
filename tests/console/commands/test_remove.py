import subprocess

import pytest

from tests.console.commands.helpers import PROJECT_ROOT, run


class TestWorkspaceRemove:
    @staticmethod
    def should_remove_specified_workspace():
        # GIVEN a workspace is being tracked
        path = "libs/my-library"
        run(["poetry", "workspace", "new", path])
        # WHEN I remove the workspace
        run(["poetry", "workspace", "remove", "my-library"])
        # THEN the workspace should no longer be tracked
        assert run(["poetry", "workspace", "list"]).text == ""
        # AND the project should still exist
        assert (PROJECT_ROOT / path).exists()

    @staticmethod
    def should_delete_when_flag_is_set():
        # GIVEN a workspace is being tracked
        path = "libs/my-library"
        run(["poetry", "workspace", "new", path])
        # WHEN I remove the workspace
        run(["poetry", "workspace", "remove", "my-library", "--delete"])
        # THEN the workspace should no longer be tracked
        assert run(["poetry", "workspace", "list"]).text == ""
        # AND the project should still exist
        assert not (PROJECT_ROOT / path).exists()

    @staticmethod
    def should_fail_when_the_specified_workspace_is_not_tracked():
        # WHEN I remove a workspace which is not tracked
        with pytest.raises(subprocess.CalledProcessError) as exc_info:
            run(["poetry", "workspace", "remove", "my-library"])
        exc = exc_info.value
        # THEN the exit code is 1
        assert exc.returncode == 1
        # AND the expected error message is displayed
        assert "Unknown workspace my-library" in exc.text, exc.text
