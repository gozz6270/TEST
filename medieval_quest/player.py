"""Player related data and helpers."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Player:
    """Represents the hero of the story."""

    name: str
    health: int = 12
    gold: int = 5
    inventory: List[str] = field(default_factory=list)

    def add_item(self, item: str) -> None:
        """Add an item to the inventory."""
        if item not in self.inventory:
            self.inventory.append(item)

    def has_item(self, item: str) -> bool:
        """Return True if the player already has the item."""
        return item in self.inventory

    def take_damage(self, amount: int) -> None:
        """Reduce the player's health by the given amount."""
        self.health = max(0, self.health - amount)

    def heal(self, amount: int) -> None:
        """Restore the player's health by the given amount."""
        self.health += amount

    def is_alive(self) -> bool:
        """Return whether the player can continue the adventure."""
        return self.health > 0
