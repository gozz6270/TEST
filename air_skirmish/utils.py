"""Utility helpers for the Air Skirmish text adventure."""

from __future__ import annotations

from textwrap import fill


def wrap(text: str) -> str:
    """Return text wrapped at 78 columns for consistent console output."""
    return fill(text, width=78)


def pause() -> None:
    """Pause the narrative until the player presses enter."""
    input("\n[계속하려면 엔터를 누르세요]")


def ask_choice(prompt: str, options: dict[str, str]) -> str:
    """Ask the player to pick an option and return the chosen key."""

    print()
    print(wrap(prompt))
    keys = list(options.keys())
    while True:
        for index, key in enumerate(keys, start=1):
            print(f"  {index}. {options[key]}")
        answer = input("선택을 입력하세요: ").strip()
        if answer.isdigit():
            idx = int(answer) - 1
            if 0 <= idx < len(keys):
                return keys[idx]
        if answer in options:
            return answer
        print("올바른 선택지를 입력해 주세요.")


__all__ = ["ask_choice", "pause", "wrap"]
