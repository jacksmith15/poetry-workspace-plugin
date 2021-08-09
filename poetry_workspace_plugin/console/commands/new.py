from pathlib import Path

from poetry.console.commands.new import NewCommand

from poetry_workspace_plugin.helpers import get_workspaces_table


class WorkspaceNewCommand(NewCommand):
    name = "workspace new"
    description = "Creates a new Python project at <path>, tracked as a workspace in the current project."

    def handle(self) -> int:

        path = Path(self.argument("path"))
        name = self.option("name") or path.name
        content = self.poetry.file.read()
        workspaces = get_workspaces_table(content)
        if name in workspaces:
            self.line(f"<fg=red>Workspace already registered with name <options=bold>{name}</></>")
            return 1
        super().handle()  # Create the new project
        workspaces[name] = str(path)
        self.poetry.file.write(content)
        return 0
