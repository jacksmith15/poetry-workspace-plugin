from cleo.commands.command import Command
from poetry.plugins.application_plugin import ApplicationPlugin


class WorkspaceCommand(Command):

    name = "workspace"

    def handle(self) -> int:
        self.line("Hello, world!")
        return 0


class WorkspacePlugin(ApplicationPlugin):
    def activate(self, application):
        application.command_loader.register_factory("workspace", WorkspaceCommand)
