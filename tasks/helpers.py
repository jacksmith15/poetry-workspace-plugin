import shutil

import poetry_workspace_plugin as package

_HEADER_LEVEL_CHARACTERS = {1: "#", 2: "=", 3: "-"}


def print_header(text: str, level: int = 1, icon: str = ""):
    icon = f" {icon} " if icon else " "

    padding_character = _HEADER_LEVEL_CHARACTERS[level]
    padding_length = max(shutil.get_terminal_size((80, 20)).columns - (len(icon) * 2), 0)
    padding = f"\n{{:{padding_character}^{padding_length}}}\n"
    if level == 1:
        text = text.upper()
    print(padding.format(f"{icon}{text}{icon}"))


__all__ = ["print_header", "package"]
