from tests.console.commands.helpers import run


def test_root_project_is_created_correctly():
    result = run(["poetry", "version"])
    assert result.text == "test-project 0.1.0"
