"""Story events for the Air Skirmish adventure."""

from __future__ import annotations

import random

from .player import Player
from .utils import ask_choice, pause, wrap


def choose_aircraft(name: str) -> Player:
    """Let the player select an aircraft and return the configured pilot."""

    options = {
        "falcon": "F-16 'Falcon' - 균형 잡힌 만능 전투기.",
        "eagle": "F-15 'Eagle' - 강력한 화력과 내구도를 자랑.",
        "raven": "KF-21 'Raven' - 첨단 센서와 연료 효율.",
    }
    choice = ask_choice(
        f"{name} 대위, 출격할 기체를 선택하세요.",
        options,
    )
    if choice == "falcon":
        return Player(name=name, aircraft="Falcon", hull=7, morale=6, fuel=7, ammo=8)
    if choice == "eagle":
        return Player(name=name, aircraft="Eagle", hull=8, morale=5, fuel=6, ammo=9)
    return Player(name=name, aircraft="Raven", hull=6, morale=6, fuel=9, ammo=7)


def pre_flight_check(player: Player) -> None:
    """First scenario where the pilot prepares for the mission."""

    print()
    print(wrap("새벽 출격을 앞두고 격납고가 분주합니다. 지휘관은 당신에게 마지막 준비 시간을 줍니다."))
    options = {
        "inspect": "기체를 꼼꼼히 점검한다 (내구도 ↑, 연료 ↓)",
        "brief": "첩보 장교와 전술 브리핑을 받는다 (사기 ↑)",
        "arm": "무장반과 탄약을 재확인한다 (탄약 ↑)",
    }
    choice = ask_choice("어떻게 시간을 사용하시겠습니까?", options)
    if choice == "inspect":
        player.adjust(hull=2, fuel=-1)
        print(wrap("정비병들과 함께 기체를 살피며 결함을 찾아냈습니다. 연료는 조금 줄었지만 마음은 든든합니다."))
    elif choice == "brief":
        player.adjust(morale=2)
        player.intel.add("지형 정보")
        print(wrap("첩보 장교가 적의 비행경로를 공유했습니다. 자신감이 솟구칩니다."))
    else:
        player.adjust(ammo=2)
        print(wrap("탄약고를 추가로 확보해 화력이 강화되었습니다."))
    pause()


def scramble_alert(player: Player) -> None:
    """Urgent scramble scenario adjusting resources based on tactics."""

    print()
    print(wrap("경보 사이렌이 울리며 긴급 출격 명령이 떨어졌습니다. 적 편대가 영공에 접근 중입니다."))
    options = {
        "afterburn": "애프터버너를 켜고 신속히 이륙한다 (연료 ↓, 사기 ↑)",
        "stealth": "레이더 피탐을 줄이며 고요하게 상승한다 (연료 ↓↓, 정보 ↑)",
        "wing": "편대와 합류해 안전하게 이동한다 (탄약 ↓, 사기 ↑)",
    }
    choice = ask_choice("이륙 방식을 선택하세요.", options)
    if choice == "afterburn":
        player.adjust(fuel=-2, morale=1)
        print(wrap("폭발적인 가속으로 가장 먼저 적을 발견했습니다!"))
    elif choice == "stealth":
        player.adjust(fuel=-3)
        player.intel.add("적 편대 배치")
        print(wrap("레이더에 포착되지 않고 고도 우위를 확보했습니다."))
    else:
        player.adjust(ammo=-1, morale=1)
        print(wrap("편대와의 호흡이 잘 맞아 사기가 올랐습니다."))
    pause()


def border_dogfight(player: Player) -> None:
    """Primary combat encounter."""

    print()
    print(wrap("북방 경계선에서 적 최신예 전투기가 나타났습니다. 치열한 공중전이 벌어집니다."))
    player.adjust(fuel=-1, ammo=-2)

    base_chance = player.morale + player.hull + (2 if "적 편대 배치" in player.intel else 0)
    base_chance += 2 if player.aircraft == "Eagle" else 0
    base_chance += 1 if "지형 정보" in player.intel else 0
    success_threshold = 16

    roll = random.randint(2, 12) + base_chance // 2
    if roll >= success_threshold:
        player.adjust(morale=2)
        player.intel.add("적 지휘 주파수")
        print(wrap("완벽한 선회 기동으로 적기를 격추했습니다! 라디오 교신도 포착했습니다."))
    elif roll >= success_threshold - 3:
        player.adjust(hull=-1, morale=-1)
        print(wrap("힘겨운 교전 끝에 적을 몰아냈습니다. 그러나 기체가 약간 손상되었습니다."))
    else:
        player.adjust(hull=-3, morale=-2)
        print(wrap("적의 미사일이 기체를 강타했습니다. 겨우 탈출했지만 큰 손상을 입었습니다."))
    pause()


def final_assault(player: Player) -> None:
    """Evaluate the final mission outcome based on the accumulated state."""

    print()
    print(wrap("적이 마지막으로 폭격기를 출격시켰습니다. 기지 방어는 당신에게 달려 있습니다."))
    player.adjust(fuel=-1, ammo=-2)

    score = player.hull + player.morale + player.fuel + player.ammo
    if "적 지휘 주파수" in player.intel:
        score += 3
    if player.aircraft == "Raven":
        score += 1

    if score >= 24:
        ending = (
            "정밀한 유도탄으로 폭격기를 격추하고 기지를 지켰습니다.",
            "당신의 이름은 공군 역사에 길이 남을 것입니다.",
        )
    elif score >= 18:
        ending = (
            "치열한 방어 끝에 적의 폭격을 막아냈습니다.",
            "기체는 손상되었지만 승리의 기쁨이 큽니다.",
        )
    elif score >= 14:
        ending = (
            "폭격을 일부 허용했지만 핵심 시설을 지켜냈습니다.",
            "분석을 통해 다음 임무를 대비해야 합니다.",
        )
    else:
        ending = (
            "연료와 탄약이 바닥나 폭격기를 저지하지 못했습니다.",
            "기지는 큰 피해를 입었지만 용감한 싸움이 기억될 것입니다.",
        )

    print()
    print(wrap(" ".join(ending)))
    print()
    print(wrap(f"최종 임무 기록 — {player.summary()}"))
    pause()


def mission_failed(player: Player) -> None:
    """Narrative used when the pilot can no longer continue."""

    print()
    print(wrap(
        "기체 상태가 한계에 도달했습니다. 더는 출격할 수 없어 즉시 귀환 명령이 내려집니다."
    ))
    print()
    print(wrap(f"현재 상태 — {player.summary()}"))
    pause()


__all__ = [
    "border_dogfight",
    "choose_aircraft",
    "final_assault",
    "mission_failed",
    "pre_flight_check",
    "scramble_alert",
]
