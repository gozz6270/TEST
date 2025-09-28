"""Player representation for the Air Skirmish game."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Player:
    """Store pilot status and resources."""

    name: str
    aircraft: str
    hull: int
    morale: int
    fuel: int
    ammo: int
    intel: set[str] = field(default_factory=set)

    def adjust(
        self,
        *,
        hull: int = 0,
        morale: int = 0,
        fuel: int = 0,
        ammo: int = 0,
    ) -> None:
        """Adjust player attributes while keeping them within sensible bounds."""

        self.hull = max(0, min(10, self.hull + hull))
        self.morale = max(0, min(10, self.morale + morale))
        self.fuel = max(0, min(10, self.fuel + fuel))
        self.ammo = max(0, min(12, self.ammo + ammo))

    def summary(self) -> str:
        """Return a short status string for the current pilot state."""

        intel = ", ".join(sorted(self.intel)) or "없음"
        return (
            f"기체 내구도: {self.hull}/10, 사기: {self.morale}/10, "
            f"연료: {self.fuel}/10, 탄약: {self.ammo}/12, 정보: {intel}"
        )

    def grounded(self) -> bool:
        """Return True if the pilot can no longer sortie."""

        return any(value <= 0 for value in (self.hull, self.morale, self.fuel, self.ammo))


__all__ = ["Player"]
