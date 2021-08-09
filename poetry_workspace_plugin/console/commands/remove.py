import shutil
from pathlib import Path

from cleo.helpers import argument, option
from poetry.console.commands.command import Command

from poetry_workspace_plugin.helpers import get_workspaces_table


class WorkspaceRemoveCommand(Command):
    arguments = [argument("name", "The target workspace to remove.")]
    options = [
        option("delete", "d", "Delete the workspace too.", flag=True),
    ]

    def handle(self) -> int:
        name = self.argument("name")
        delete = self.option("delete")
        content = self.poetry.file.read()
        workspaces = get_workspaces_table(content)

        if name not in workspaces:
            self.line(f"<fg=red>Unknown workspace <options=bold>{name}</></>")
            return 1
        path = Path(workspaces[name])  # type: ignore[arg-type]
        del workspaces[name]
        self.poetry.file.write(content)
        if delete and path.exists():
            shutil.rmtree(path)
        return 0
