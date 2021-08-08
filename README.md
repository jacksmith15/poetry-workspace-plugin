# poetry-workspace-plugin
Poetry workspace plugin - for Python monorepos.

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
