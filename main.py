"""Entry point for the Air Skirmish text adventure."""

from __future__ import annotations

from air_skirmish.game import Game


def main() -> None:
    """Run the Air Skirmish game."""

    Game().run()


if __name__ == "__main__":
    main()
