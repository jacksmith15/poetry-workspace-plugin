import subprocess

from cleo.helpers import argument, option
from poetry.console.commands.command import Command

from poetry_workspace_plugin.helpers import get_workspaces_table


class WorkspaceRunCommand(Command):
    name = "workspace run"
    description = "Runs command in every workspace tracked by this project."

    arguments = [argument("args", "The command and arguments/options to run.", multiple=True)]
    options = [
        option(
            "targets",
            "t",
            "Comma-separated list of target workspaces by name. Omit to run the command in all tracked workspaces.",
            flag=False,
            default=None,
        )
    ]

    def handle(self) -> int:
        args = self.argument("args")
        workspaces = get_workspaces_table(self.poetry.file.read())

        targets = self.option("targets")
        if targets:
            targets = set(targets.split(","))
            if unexpected := (targets - set(workspaces)):
                self.line(f"<fg=red>Unknown workspaces: <options=bold>{','.join(unexpected)}</></>")
                return 1
        else:
            targets = set(workspaces)

        if not workspaces:
            self.line("<c1>No workspaces tracked by this project</>")
            return 0

        for target in targets:
            if exit_code := self._run_in_workspace(workspaces[target], args):  # type: ignore[arg-type]
                return exit_code
        return 0

    def _run_in_workspace(self, workspace_path: str, args: list[str]):
        self.line(f"<comment>Running 'poetry run {' '.join(args)}' in '{workspace_path}'</>")
        exe = subprocess.Popen(args, cwd=workspace_path)
        exe.communicate()
        return exe.returncode
