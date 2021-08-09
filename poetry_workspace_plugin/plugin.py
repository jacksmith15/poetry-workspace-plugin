from poetry.plugins.application_plugin import ApplicationPlugin

from poetry_workspace_plugin.console.commands.add import WorkspaceAddCommand
from poetry_workspace_plugin.console.commands.list import WorkspaceListCommand
from poetry_workspace_plugin.console.commands.new import WorkspaceNewCommand


class WorkspacePlugin(ApplicationPlugin):
    def activate(self, application):
        application.command_loader.register_factory("workspace new", WorkspaceNewCommand)
        application.command_loader.register_factory("workspace add", WorkspaceAddCommand)
        application.command_loader.register_factory("workspace list", WorkspaceListCommand)
