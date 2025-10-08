"""Entry point for the Medieval Quest text adventure."""
from __future__ import annotations

from medieval_quest import Game


def main() -> None:
    """Run the Medieval Quest game."""
    Game().run()


if __name__ == "__main__":
    main()
