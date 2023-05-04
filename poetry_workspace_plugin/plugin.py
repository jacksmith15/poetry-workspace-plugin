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

    def activate(self, application):
        # Operating at a workspace level:
        application.command_loader.register_factory("workspace new", WorkspaceNewCommand)
        application.command_loader.register_factory("workspace list", WorkspaceListCommand)
        application.command_loader.register_factory("workspace dependees", WorkspaceDependeesCommand)

        # Overriden commands which work differently on packages inside a workspace:

        ## Members of a workspace can only add/remove dependencies from the workspace global lockfile
        application.command_loader.register_factory("add", AddCommand)
        application.command_loader.register_factory("remove", WorkspaceRemoveCommand)

        ## Members of a workspace install using the shared lockfile
        application.command_loafer.register_factory("install", InstallCommand)

        ## Members of a workspace don't have their own lockfile:
        application.command_loader.register_factory("update", UpdateCommand)
        application.command_loader.register_factory("lock", LockCommand)

        ## Packaged workspace members should draw dependency versions from the root pyproject
        application.command_loader.register_factory("build", BuildCommand)
