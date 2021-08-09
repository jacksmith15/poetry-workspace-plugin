import subprocess

from cleo.commands.command import Command
from cleo.helpers import argument

from poetry_workspace_plugin.helpers import get_workspaces_table


class WorkspaceRunCommand(Command):
    name = "workspace run"
    description = "Runs command in every workspace tracked by this project."

    arguments = [argument("args", "The command and arguments/options to run.", multiple=True)]

    def handle(self) -> int:
        args = self.argument("args")
        workspaces = get_workspaces_table(self.poetry.file.read())
        if not workspaces:
            self.line("<c1>No workspaces tracked by this project</>")
            return 0

        for path in workspaces.values():
            if exit_code := self._run_in_workspace(path, args):
                return exit_code
        return 0

    def _run_in_workspace(self, workspace_path: str, args: list[str]):
        self.line(f"<comment>Running 'poetry run {' '.join(args)}' in '{workspace_path}'</>")
        exe = subprocess.Popen(args, cwd=workspace_path)
        exe.communicate()
        return exe.returncode
