from cleo.commands.command import Command


class WorkspaceListCommand(Command):
    name = "workspace list"
    description = "Lists workspaces tracked in current project."

    def handle(self) -> int:
        # Read current pyproject.toml
        content = self.poetry.file.read()
        poetry_content = content["tool"]["poetry"]
        if "workspaces" not in poetry_content:
            return 0

        table = self.table(style="compact")
        table.add_rows([["<c1>{}</>".format(name), path] for name, path in poetry_content["workspaces"].items()])
        table.render()
        return 0
