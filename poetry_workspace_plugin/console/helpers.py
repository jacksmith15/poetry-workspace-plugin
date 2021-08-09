from tomlkit import inline_table, table
from tomlkit.items import InlineTable, Table
from tomlkit.toml_document import TOMLDocument


def get_workspaces_table(pyproject: TOMLDocument) -> InlineTable:
    return get_workspace_section(pyproject).setdefault("workspaces", inline_table())  # type: ignore


def get_workspace_section(pyproject: TOMLDocument) -> Table:
    return pyproject["tool"]["poetry"].setdefault("workspace", table())  # type: ignore
