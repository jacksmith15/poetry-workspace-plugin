from pathlib import Path

from cleo.helpers import option
from cleo.io.outputs.output import Verbosity
from poetry.console.commands.command import Command
from poetry.factory import Factory
from poetry.core.masonry.builder import Builder
from poetry.core.packages.dependency import Dependency
from poetry.core.packages.directory_dependency import DirectoryDependency
from poetry.utils.env import EnvManager

from poetry_workspace_plugin.helpers import get_workspaces_table, get_parent, get_dependency_range, \
    get_dependency_ranges


class WorkspaceBuildCommand(Command):
    name = "workspace build"
    description = "Builds each workspace package, as a tarball and a wheel by default."

    options = [
        option("format", "f", "Limit the format to either sdist or wheel.", flag=False),
        option(
            "targets",
            "t",
            "Comma-separated list of target workspaces by name. Omit to run the command in all tracked workspaces.",
            flag=False,
            default=None,
        )
    ]

    help = """The build command builds workspace packages.

If invoked in a workspace, it builds the current workspace, resolving any directory dependency pointing to another
workspace to a regular dependency using its version number.

When invoked in the workspaces root, it will build all of its workspaces.
"""

    def handle(self) -> int:
        parent = get_parent(self.poetry.file.read())
        workspaces = get_workspaces_table(self.poetry.file.read())

        fmt = self.option("format") or "all"

        if parent:
            parent_path = Path(parent).resolve()
            parent_poetry = Factory().create_poetry(parent_path, io=self.io)
            self._build_workspace(parent_poetry, self.poetry, fmt)

        elif workspaces:
            for ws, path in workspaces.items():
                workspace_poetry = Factory().create_poetry(Path(path).resolve(), io=self.io)
                self.line(f"Changing workspace to <c1>{ws}</c1>", verbosity=Verbosity.VERBOSE)
                self._build_workspace(self.poetry, workspace_poetry, fmt)

        else:
            self.line(f"Not in workspace, falling back to regular build.")
            self.call("build")

        return 0

    def _build(self, poetry, fmt):
        package = poetry.package
        self.line(
            f"Building <c1>{package.pretty_name}</c1> (<c2>{package.version}</c2>)"
        )
        io = self.io

        env_manager = EnvManager(poetry)
        env = env_manager.create_venv(io)

        if env.is_venv() and io.is_verbose():
            io.write_line(f"Using virtualenv: <comment>{env.path}</>")

        builder = Builder(poetry)
        builder.build(fmt, executable=env.python)

    def _workspace_dependency_constraint(self, workspace, version, file) -> str:
        dependency_range = ""
        default_dependency_range = get_dependency_range(file)
        if default_dependency_range is not None:
            dependency_range = default_dependency_range
        workspace_dependency_range = get_dependency_ranges(file).get(workspace)
        if workspace_dependency_range is not None:
            dependency_range = workspace_dependency_range

        if dependency_range == "*":
            return dependency_range
        elif dependency_range == "~" or dependency_range == "^" or dependency_range == "":
            return f"{dependency_range}{version}"
        else:
            raise AssertionError(f"Dependency range constraint '{dependency_range}' not supported")

    def _build_workspace(self, root, workspace, fmt):
        workspaces = get_workspaces_table(root.file.read())
        package = workspace.package

        ws_deps = {}
        for dependency in package.requires:
            dep_name = dependency.name
            if dep_name in workspaces and \
                    dep_name not in ws_deps:
                ws_dep_path = root.file.parent.joinpath(workspaces[dep_name])
                project = Factory().create_poetry(ws_dep_path, io=self.io)
                ws_deps[dep_name] = (dependency, project)

        # rewrite directory dependencies to versioned dependencies
        for name, (dependency, project) in ws_deps.items():
            if isinstance(dependency, DirectoryDependency):
                constraint = self._workspace_dependency_constraint(name, project.package.version, workspace.file.read())
                regular_dep = Dependency(
                    name=dependency.name,
                    constraint=constraint,
                    groups=dependency.groups,
                    optional=dependency._optional,
                    allows_prereleases=True,
                    extras=dependency.extras
                )
                for group in dependency.groups:
                    package.dependency_group(group).remove_dependency(dependency.name)
                    package.dependency_group(group).add_dependency(regular_dep)

        self._build(workspace, fmt)
