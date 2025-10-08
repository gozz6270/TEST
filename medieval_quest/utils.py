"""Utility helpers for the medieval quest game."""
from __future__ import annotations

import os
from typing import Iterable, Tuple, TypeVar

Choice = TypeVar("Choice")


def clear_screen() -> None:
    """Attempt to clear the terminal screen."""
    command = "cls" if os.name == "nt" else "clear"
    os.system(command)


def print_divider(width: int = 60, char: str = "=") -> None:
    """Print a decorative divider line."""
    print(char * width)


def prompt_choice(prompt: str, options: Iterable[Tuple[str, Choice]]) -> Choice:
    """Prompt the player to select one of the provided options."""
    choices = list(options)
    if not choices:
        raise ValueError("options must not be empty")

    print(prompt)
    for index, (label, _) in enumerate(choices, start=1):
        print(f"  {index}. {label}")

    while True:
        selection = input("번호를 선택하세요: ").strip()
        if selection.isdigit():
            idx = int(selection) - 1
            if 0 <= idx < len(choices):
                _, value = choices[idx]
                return value
        print("올바른 번호를 입력해주세요.")


def prompt_continue(message: str = "계속하려면 Enter 키를 누르세요...") -> None:
    """Pause until the player presses Enter."""
    input(message)


def format_inventory(items: Iterable[str]) -> str:
    """Format the inventory into a comma separated string."""
    items = list(items)
    return ", ".join(items) if items else "(비어 있음)"
