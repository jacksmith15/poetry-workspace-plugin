from tomlkit import inline_table, table
from tomlkit.items import InlineTable, Table
from tomlkit.toml_document import TOMLDocument


def get_workspaces_table(pyproject: TOMLDocument) -> InlineTable:
    workspace_section = get_workspace_section(pyproject)
    if "workspaces" not in workspace_section:
        workspace_section["workspaces"] = inline_table()
    return workspace_section["workspaces"]  # type: ignore


def get_workspace_section(pyproject: TOMLDocument) -> Table:
    poetry_section = pyproject["tool"]["poetry"]  # type: ignore
    if "workspace" not in poetry_section:  # type: ignore
        poetry_section["workspace"] = table()  # type: ignore
    return poetry_section["workspace"]  # type: ignore
