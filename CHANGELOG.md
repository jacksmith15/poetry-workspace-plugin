# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog] and this project adheres to
[Semantic Versioning].

Types of changes are:
* **Security** in case of vulnerabilities.
* **Deprecated** for soon-to-be removed features.
* **Added** for new features.
* **Changed** for changes in existing functionality.
* **Removed** for now removed features.
* **Fixed** for any bug fixes.

## [Unreleased]
### Added
* Project started :)
* Proof-of-concept CLI for managing multiple poetry projects as 'workspaces'.
  - `poetry workspace new` creates a new workspace
  - `poetry workspace add` tracks an existing project as a workspace
  - `poetry workspace list` shows currently tracked workspaces
  - `poetry workspace remove` untracks a workspace
  - `poetry workspace run` runs a command in multiple workspaces
  - `poetry workspace dependees` lists workspaces which depend on specified workspaces

[Unreleased]: https://github.com/jacksmith15/poetry-workspace-plugin/compare/initial..HEAD

[Keep a Changelog]: http://keepachangelog.com/en/1.0.0/
[Semantic Versioning]: http://semver.org/spec/v2.0.0.html

[_release_link_format]: https://github.com/jacksmith15/poetry-workspace-plugin/compare/{previous_tag}..{tag}
[_breaking_change_token]: BREAKING
