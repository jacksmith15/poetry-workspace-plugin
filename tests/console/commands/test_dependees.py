import subprocess

import pytest

from tests.console.commands.helpers import run


class TestWorkspaceDependees:
    @staticmethod
    def should_identify_direct_dependees():
        # GIVEN I have three workspaces
        paths = {"libs/library-one", "libs/library-two", "libs/library-three"}
        for path in paths:
            run(["poetry", "workspace", "new", path])
        # AND one of them depends on the other
        run(["poetry", "add", "../library-one"], cwd="libs/library-two")
        # WHEN I run workspace dependees on the dependency workspace
        result = run(["poetry", "workspace", "dependees", "library-one"])
        # THEN the target and dependent workspace should be included in the result
        assert set(result.text.splitlines()) == {"library-one", "library-two"}

    @staticmethod
    def should_identify_transitive_dependees():
        # GIVEN I have four workspaces
        paths = {"libs/library-one", "libs/library-two", "libs/library-three", "libs/library-four"}
        for path in paths:
            run(["poetry", "workspace", "new", path])
        # AND the first depends on the second
        run(["poetry", "add", "../library-two"], cwd="libs/library-one")
        # AND the second depends on the third
        run(["poetry", "add", "../library-three"], cwd="libs/library-two")
        # WHEN I run workspace dependees on the third workspace
        result = run(["poetry", "workspace", "dependees", "library-three"])
        # THEN the first three should be included in the result
        assert set(result.text.splitlines()) == {"library-one", "library-two", "library-three"}

    @staticmethod
    def should_ignore_transitive_dependees_when_specified():
        # GIVEN I have four workspaces
        paths = {"libs/library-one", "libs/library-two", "libs/library-three", "libs/library-four"}
        for path in paths:
            run(["poetry", "workspace", "new", path])
        # AND the first depends on the second
        run(["poetry", "add", "../library-two"], cwd="libs/library-one")
        # AND the second depends on the third
        run(["poetry", "add", "../library-three"], cwd="libs/library-two")
        # WHEN I run workspace dependees with the --no-transitive flag on the third workspace
        result = run(["poetry", "workspace", "dependees", "--no-transitive", "library-three"])
        # THEN only the second two should be included in the result
        assert set(result.text.splitlines()) == {"library-two", "library-three"}

    @staticmethod
    def should_return_csv_format_when_specified():
        # GIVEN I have two workspaces
        paths = {"libs/library-one", "libs/library-two"}
        for path in paths:
            run(["poetry", "workspace", "new", path])
        # AND one of them depends on the other
        run(["poetry", "add", "../library-one"], cwd="libs/library-two")
        # WHEN I run workspace dependees on the dependency workspace
        result = run(["poetry", "workspace", "dependees", "--csv", "library-one"])
        # THEN the result should be in csv format
        assert result.text == "library-one,library-two"

    @staticmethod
    def should_fail_when_unknown_workspaces_are_referenced():
        # WHEN I run workspace dependees with an unknown workspace
        with pytest.raises(subprocess.CalledProcessError) as exc_info:
            run(["poetry", "workspace", "dependees", "library-one"])
        exc = exc_info.value
        # THEN the exit code is 1
        assert exc.returncode == 1
        # AND the expected error message is displayed
        assert "Unknown workspace: library-one" in exc.text
