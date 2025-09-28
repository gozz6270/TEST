"""Medieval text adventure game.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from textwrap import fill


def wrap(text: str) -> str:
    """Return text wrapped at 78 characters."""
    return fill(text, width=78)


def pause() -> None:
    """Pause the game until the player presses enter."""
    input("\n[계속하려면 엔터를 누르세요]")


def ask_choice(prompt: str, options: dict[str, str]) -> str:
    """Ask the player to pick among several options.

    Args:
        prompt: The narrative leading to the choice.
        options: A dictionary mapping option keys to text.

    Returns:
        The key chosen by the player.
    """

    print()
    print(wrap(prompt))
    keys = list(options.keys())
    while True:
        for idx, key in enumerate(keys, start=1):
            print(f"  {idx}. {options[key]}")
        answer = input("선택을 입력하세요: ").strip()
        if answer.isdigit():
            index = int(answer) - 1
            if 0 <= index < len(keys):
                return keys[index]
        if answer in options:
            return answer
        print("올바른 선택지를 입력해 주세요.")


@dataclass
class Player:
    name: str
    role: str
    prestige: int
    morale: int
    wealth: int
    inventory: set[str] = field(default_factory=set)

    def adjust(self, *, prestige: int = 0, morale: int = 0, wealth: int = 0) -> None:
        self.prestige = max(0, self.prestige + prestige)
        self.morale = max(0, self.morale + morale)
        self.wealth = max(0, self.wealth + wealth)

    def summary(self) -> str:
        return (
            f"명성: {self.prestige}, 사기: {self.morale}, 재정: {self.wealth}, "
            f"소지품: {', '.join(sorted(self.inventory)) or '없음'}"
        )


def choose_role(name: str) -> Player:
    options = {
        "knight": "기사 - 높은 사기와 명성을 얻지만 재정이 부족합니다.",
        "merchant": "상인 - 재정과 교섭술이 뛰어납니다.",
        "scholar": "학자 - 지식과 명성이 있어 왕실의 신뢰를 받습니다.",
    }
    choice = ask_choice(
        f"{name} 님, 카스텔 로단 왕국을 지킬 신하로 임명되었습니다. 어떤 역할로 봉사하시겠습니까?",
        options,
    )
    if choice == "knight":
        return Player(name=name, role="기사", prestige=3, morale=5, wealth=2)
    if choice == "merchant":
        return Player(name=name, role="상인", prestige=2, morale=3, wealth=6)
    return Player(name=name, role="학자", prestige=4, morale=3, wealth=3)


def tournament(player: Player) -> None:
    print()
    print(wrap("봄맞이 토너먼트가 열렸습니다. 이는 왕국의 단결을 다지는 중요한 행사입니다."))
    if player.role == "기사":
        prompt = "검술 대회에 참가해 명예를 노리시겠습니까, 아니면 병사들과 함께 훈련하시겠습니까?"
        choice = ask_choice(prompt, {
            "duel": "대회에 참가한다",
            "train": "병사들과 합동 훈련을 한다",
        })
        if choice == "duel":
            result = random.random()
            if result < 0.6:
                player.adjust(prestige=2)
                print(wrap("멋진 승리로 백성들의 환호를 받았습니다! 명성이 올랐습니다."))
            else:
                player.adjust(morale=-1)
                print(wrap("안타깝게도 부상으로 쓰러졌습니다. 사기가 떨어졌습니다."))
        else:
            player.adjust(morale=2)
            print(wrap("병사들이 당신의 격려에 감동해 사기가 크게 올랐습니다."))
    else:
        prompt = "행사를 후원하여 백성들의 마음을 사시겠습니까, 아니면 왕과의 연회에 집중하시겠습니까?"
        choice = ask_choice(prompt, {
            "sponsor": "토너먼트를 후원한다",
            "court": "왕과 신료들을 공략한다",
        })
        if choice == "sponsor":
            if player.wealth >= 3:
                player.adjust(wealth=-3, morale=2)
                print(wrap("넉넉한 지원으로 백성들이 당신을 두고두고 칭송합니다."))
            else:
                player.adjust(morale=-1)
                print(wrap("자금이 부족해 제대로 후원하지 못했습니다. 실망한 백성들이 떠납니다."))
        else:
            player.adjust(prestige=1)
            player.inventory.add("왕의 신임")
            print(wrap("연회에서 현명한 조언을 건네어 왕의 신임을 얻었습니다."))
    pause()


def tavern_intel(player: Player) -> None:
    print()
    print(wrap("성 주변의 주점에서 국경을 넘나드는 용병들이 수상한 소문을 퍼뜨리고 있습니다."))
    options = {
        "bribe": "금을 뿌려 소문을 캐낸다",
        "shadow": "몰래 뒤따라 움직임을 살핀다",
        "ignore": "소문을 무시하고 성으로 돌아간다",
    }
    choice = ask_choice("어떻게 하시겠습니까?", options)
    if choice == "bribe":
        cost = 2 if player.role == "상인" else 3
        if player.wealth >= cost:
            player.adjust(wealth=-cost, prestige=1)
            player.inventory.add("첩보")
            print(wrap("비싼 값이었지만 침략 계획을 담은 문서를 확보했습니다."))
        else:
            player.adjust(prestige=-1)
            print(wrap("지불 능력이 없다는 소문이 퍼져 체면을 구겼습니다."))
    elif choice == "shadow":
        success = random.random() < (0.5 if player.role == "기사" else 0.3)
        if success:
            player.adjust(morale=1)
            player.inventory.add("비밀 통로")
            print(wrap("몰래 뒤따르다 성으로 이어지는 비밀 통로를 발견했습니다!"))
        else:
            player.adjust(morale=-2)
            print(wrap("발각되어 곤욕을 치렀습니다. 용병들에게 모욕을 당했습니다."))
    else:
        player.adjust(morale=1 if player.role == "학자" else 0)
        print(wrap("무모한 행동을 피했습니다. 대신 전략서 연구에 집중합니다."))
    pause()


def council_meeting(player: Player) -> None:
    print()
    print(wrap("침략의 조짐이 포착되자, 왕국의 원로회가 긴급 소집되었습니다."))
    options = {
        "fortify": "성벽을 보강하자고 주장한다",
        "rally": "백성과 기사들에게 연설한다",
        "diplomacy": "이웃 왕국과 동맹을 추진한다",
    }
    choice = ask_choice("회의에서 어떤 전략을 제시하시겠습니까?", options)
    if choice == "fortify":
        bonus = 2 if "비밀 통로" in player.inventory else 0
        player.adjust(prestige=1 + bonus // 2)
        print(wrap("세부적인 설계로 성벽 강화 계획을 이끌었습니다. 신뢰가 높아집니다."))
    elif choice == "rally":
        boost = 3 if player.role == "기사" else 2
        player.adjust(morale=boost)
        print(wrap("불타는 연설로 군심을 다잡았습니다. 병사들이 전투를 갈망합니다."))
    else:
        if "왕의 신임" in player.inventory:
            player.adjust(prestige=2, wealth=1)
            print(wrap("왕의 신임을 활용해 신속히 사절단을 파견했습니다. 보급품이 도착합니다."))
        else:
            player.adjust(prestige=-1)
            print(wrap("신임이 부족해 동맹 추진이 좌절되었습니다. 동료들이 실망합니다."))
    pause()


def final_battle(player: Player) -> None:
    print()
    print(wrap("드디어 북방 연합군이 성문 앞에 도달했습니다. 당신의 선택이 결전의 결과를 좌우합니다."))
    strength = player.prestige + player.morale + (2 if "첩보" in player.inventory else 0)
    strength += 2 if "비밀 통로" in player.inventory else 0
    strength += player.wealth // 2

    if strength >= 15:
        ending = (
            "당신의 지휘 아래 왕국은 눈부신 승리를 거두었습니다."
            " 전설 속 영웅으로 이름이 남습니다."
        )
    elif strength >= 11:
        ending = (
            "치열한 전투 끝에 연합군을 물리쳤습니다."
            " 왕과 백성들이 당신에게 깊은 감사를 표합니다."
        )
    elif strength >= 8:
        ending = (
            "전투는 가까스로 승리했지만 큰 희생을 치렀습니다."
            " 앞으로 더 많은 준비가 필요해 보입니다."
        )
    else:
        ending = (
            "성은 함락되었고 왕국은 연합군에게 무릎을 꿇었습니다."
            " 그러나 당신의 저항은 후대에 용기로 기억될 것입니다."
        )

    print()
    print(wrap(ending))
    print()
    print(wrap(f"최종 기록 — {player.summary()}"))


def main() -> None:
    print(wrap("카스텔 로단 왕국에 오신 것을 환영합니다! 중세 시대의 격동 속에서 왕국의 "
               "운명을 책임질 모험을 시작해 보세요."))
    name = input("당신의 이름은 무엇입니까? ").strip() or "이름 없는 영웅"
    player = choose_role(name)
    print()
    print(wrap(f"{player.role} {player.name} 님, 왕국의 운명이 당신의 손에 달렸습니다."))
    print(wrap(f"현재 상태 — {player.summary()}"))
    pause()

    tournament(player)
    tavern_intel(player)
    council_meeting(player)
    final_battle(player)

    print()
    print(wrap("모험이 여기서 끝났습니다. 다시 도전하고 싶다면 게임을 다시 실행하세요!"))


if __name__ == "__main__":
    main()
