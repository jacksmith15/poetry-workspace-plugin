# poetry-workspace-plugin

Poetry workspace plugin for Python monorepos.

Adds a new subcommand group, `poetry workspace`, which is used to create, manage and inspect nested Python projects.

```shell
# Create a new python project at the specified path, tracked in the current project
poetry workspace new libs/my-library

# Add an existing python project to the current project's workspaces
poetry workspace add libs/my-existing-library

# List the current workspaces
poetry workspace list

# Run a command in every workspace:
poetry workspace run command

# Run a command in specified workspaces:
poetry workspace run --targets=my-library,my-existing-library -- command

# List dependees of a particular workspace (from among the list of workspaces).
poetry workspace dependees my-library

# Unlink a workspace from the current project
poetry remove workspace my-library

# Unlink and delete a workspace from the current project
poetry remove workspace my-library --delete
```

### Common patterns

#### Testing affected workspaces

After making a change to a workspace, you can run tests for all _affected_ workspaces like so:
```shell
poetry workspace run --targets=$(poetry workspace dependees my-library) -- pytest tests/
```

### Planned commands

The following are currently possible e.g via `poetry workspace run poetry build`, but this would be more succint:

```shell
# Build or publish all workspaces:
poetry workspace build
poetry workspace publish

# Build specified workspaces:
poetry workspace --targets=my-library build

# Publish specified workspaces:
poetry workspace --targets=my-library publish
```


Metadata regarding workspaces is stored under `tool.poetry.workspaces`:

```toml
[tool.poetry.workspace]
workspaces = {
    my-library = "libs/my-library"
}
```

## Installation

This project is not currently packaged and so must be installed manually.

Clone the project with the following command:
```
git clone https://github.com/jacksmith15/poetry-workspace-plugin.git
```

## Development

Install dependencies:

```shell
pyenv shell 3.9.4  # Or other 3.9.x
pre-commit install  # Configure commit hooks
poetry install  # Install Python dependencies
```

Run tests:

```shell
poetry run inv verify
```

# License
This project is distributed under the MIT license.
