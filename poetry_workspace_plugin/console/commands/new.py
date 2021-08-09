from pathlib import Path

from poetry.console.commands.new import NewCommand


class WorkspaceNewCommand(NewCommand):
    name = "workspace new"
    description = "Creates a new Python project at <path>, tracked as a workspace in the current project."

    def handle(self) -> int:
        from tomlkit import table

        path = Path(self.argument("path"))
        name = self.option("name") or path.name
        content = self.poetry.file.read()
        poetry_content = content["tool"]["poetry"]
        if "workspaces" not in poetry_content:
            poetry_content["workspaces"] = table()
        section = poetry_content["workspaces"]
        if name in section:
            self.line(f"<fg=red>Workspace already registered with name <options=bold>{name}</></>")
            return 1
        super().handle()  # Create the new project
        section[name] = path
        self.poetry.file.write(content)
        return 0
