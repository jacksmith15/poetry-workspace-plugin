import subprocess
from pathlib import Path
from typing import Union

from tests.console.commands.constants import PROJECT_ROOT


def run(args: list[str], cwd: Union[Path, str] = PROJECT_ROOT):
    """Run a command from within the test project root."""
    cwd = Path(cwd)
    if not cwd.is_absolute():
        cwd = PROJECT_ROOT / cwd

    def format_output(stdout: bytes, stderr: bytes) -> str:
        return "\n".join(
            [
                stdout.decode().strip(),
                stderr.decode().strip(),
            ]
        ).strip()

    try:
        result = subprocess.run(args, check=True, capture_output=True, cwd=cwd)
    except subprocess.CalledProcessError as exc:
        exc.text = format_output(exc.stdout, exc.stderr)  # type: ignore[attr-defined]
        raise exc
    result.text = format_output(result.stdout, result.stderr)  # type: ignore[attr-defined]
    return result
