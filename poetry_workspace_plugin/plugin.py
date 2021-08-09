from poetry.plugins.application_plugin import ApplicationPlugin

from poetry_workspace_plugin.console.commands.add import WorkspaceAddCommand
from poetry_workspace_plugin.console.commands.dependees import WorkspaceDependeesCommand
from poetry_workspace_plugin.console.commands.list import WorkspaceListCommand
from poetry_workspace_plugin.console.commands.new import WorkspaceNewCommand
from poetry_workspace_plugin.console.commands.remove import WorkspaceRemoveCommand
from poetry_workspace_plugin.console.commands.run import WorkspaceRunCommand


class WorkspacePlugin(ApplicationPlugin):
    def activate(self, application):
        application.command_loader.register_factory("workspace new", WorkspaceNewCommand)
        application.command_loader.register_factory("workspace add", WorkspaceAddCommand)
        application.command_loader.register_factory("workspace list", WorkspaceListCommand)
        application.command_loader.register_factory("workspace run", WorkspaceRunCommand)
        application.command_loader.register_factory("workspace remove", WorkspaceRemoveCommand)
        application.command_loader.register_factory("workspace dependees", WorkspaceDependeesCommand)
