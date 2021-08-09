from pathlib import Path

from cleo.commands.command import Command
from cleo.helpers import argument


class WorkspaceAddCommand(Command):
    name = "workspace add"
    description = "Begins tracking an existing Python project at <path> as a workspace."

    arguments = [argument("path", "The path to the Python project")]

    def handle(self) -> int:
        from tomlkit import table

        # Check path is a valid project
        path = Path(self.argument("path"))
        name = self._get_target_project_name(path)
        self._validate_path(path)

        # Read current pyproject.toml
        content = self.poetry.file.read()
        poetry_content = content["tool"]["poetry"]
        if "workspaces" not in poetry_content:
            poetry_content["workspaces"] = table()
        section = poetry_content["workspaces"]

        # Check that name is already used
        if name in section:
            self.line(f"<fg=red>Workspace already registered with name <options=bold>{name}</></>")
            return 1

        # Add the new workspace to current pyproject.toml
        section[name] = path
        self.poetry.file.write(content)
        return 0

    @staticmethod
    def _get_target_project_name(path: Path) -> str:
        from poetry.core.factory import Factory
        from poetry.core.pyproject.toml import PyProjectTOML

        poetry_file = path / "pyproject.toml"
        if not poetry_file.exists():
            raise RuntimeError(f"Poetry could not find a pyproject.toml file in {path!r} or its parents")

        pyproject = PyProjectTOML(path=poetry_file)
        local_config = pyproject.poetry_config

        # Checking validity
        check_result = Factory.validate(local_config)
        if check_result["errors"]:
            message = ""
            for error in check_result["errors"]:
                message += "  - {}\n".format(error)

            raise RuntimeError("The Poetry configuration is invalid:\n" + message)
        return pyproject.data["name"]
