"""Main game controller for Air Skirmish."""

from __future__ import annotations

from . import scenarios
from .player import Player
from .utils import pause, wrap


class Game:
    """Coordinate the narrative flow of the air skirmish adventure."""

    def __init__(self) -> None:
        self.player: Player | None = None

    def run(self) -> None:
        """Run the full game loop."""

        print(wrap(
            "공군 비상출격 시뮬레이터 'Air Skirmish'에 오신 것을 환영합니다! "
            "당신은 최전선 비행대의 리더로서 기지를 지켜야 합니다."
        ))
        name = input("조종사 이름을 입력하세요: ").strip() or "이름 없는 파일럿"
        self.player = scenarios.choose_aircraft(name)
        print()
        print(wrap(f"선택한 기체: {self.player.aircraft}. 행운을 빕니다, {self.player.name} 대위."))
        print(wrap(f"현재 상태 — {self.player.summary()}"))
        pause()

        self._play_mission()

    def _play_mission(self) -> None:
        assert self.player is not None
        player = self.player

        scenarios.pre_flight_check(player)
        if player.grounded():
            scenarios.mission_failed(player)
            return

        scenarios.scramble_alert(player)
        if player.grounded():
            scenarios.mission_failed(player)
            return

        scenarios.border_dogfight(player)
        if player.grounded():
            scenarios.mission_failed(player)
            return

        scenarios.final_assault(player)
        print()
        print(wrap("임무가 종료되었습니다. 새로운 선택으로 다시 도전해 보세요!"))
        pause()


__all__ = ["Game"]
