from collections import defaultdict
from functools import cached_property
from pathlib import Path

from cleo.helpers import argument, option
from poetry.console.commands.command import Command
from poetry.core.pyproject.toml import PyProjectTOML

from poetry_workspace_plugin.helpers import get_workspaces_table

# TODO: group dependees?


class WorkspaceDependeesCommand(Command):
    name = "workspace dependees"
    description = "List workspaces which depend on the specified workspaces."

    arguments = [argument("targets", "The workspaces to compute dependees of, by name", multiple=True)]
    options = [
        option("no-transitive", None, "Only show the immediate dependees", flag=True),
        option("csv", None, "Return comma-separated list", flag=True),
    ]

    def handle(self) -> int:
        targets = set(self.argument("targets"))
        transitive = not self.option("no-transitive")
        workspaces = get_workspaces_table(self.poetry.file.read())
        if unexpected := (targets - set(workspaces)):
            self.line(f"<fg=red>Unknown workspaces: <options=bold>{','.join(unexpected)}</></>")
            return 1
        dependees = targets.union(*[self._find_dependees(name, transitive=transitive) for name in targets])

        if self.option("csv"):
            self.line(",".join(dependees))
            return 0

        for dependee in dependees:
            self.line(dependee)
        return 0

    def _find_dependees(self, name: str, transitive: bool = True) -> set[str]:
        dependees = self._dependee_map[name]
        if not transitive:
            return dependees
        for dependee in dependees:
            dependees |= self._find_dependees(dependee)
        return dependees

    @cached_property
    def _dependee_map(self) -> dict[str, set[str]]:
        result = defaultdict(set)
        for name in self._workspaces:
            for dependency_name in self._get_workspace_direct_dependencies(name):
                result[dependency_name].add(name)
        return result

    def _get_workspace_direct_dependencies(self, name: str) -> set[str]:
        path = Path(self._workspaces[name])
        poetry_file = path / "pyproject.toml"
        if not poetry_file.exists():
            raise RuntimeError(f"Poetry could not find a pyproject.toml file in {path!r}")
        pyproject = PyProjectTOML(path=poetry_file).file.read()
        dependencies = pyproject["tool"]["poetry"]["dependencies"]

        result = set()
        for key, value in dependencies.items():
            if isinstance(value, dict) and "path" in value:
                target_path = (path / value["path"]).resolve()
                if target_path in self._workspace_absolute_paths:
                    result.add(self._workspace_absolute_paths[target_path])
        return result

    @cached_property
    def _workspace_absolute_paths(self) -> dict[Path, str]:
        return {Path(path).resolve(): name for name, path in self._workspaces.items()}

    @cached_property
    def _workspaces(self) -> dict[str, str]:
        return get_workspaces_table(self.poetry.file.read())  # type: ignore[return-value]
