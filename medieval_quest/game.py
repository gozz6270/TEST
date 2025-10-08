"""Core gameplay loop for the medieval quest adventure."""
from __future__ import annotations

from typing import Callable, Dict, Optional

from . import scenarios, utils
from .player import Player

SceneHandler = Callable[[], Optional[str]]


class Game:
    """A simple text-based adventure set in a medieval kingdom."""

    def __init__(self) -> None:
        self.player: Optional[Player] = None
        self.scenes: Dict[str, SceneHandler] = {
            "intro": self.scene_intro,
            "council": self.scene_council,
            "market": self.scene_market,
            "forest": self.scene_forest,
            "bandit": self.scene_bandit,
            "shrine": self.scene_shrine,
            "ruins": self.scene_ruins,
            "dragon": self.scene_dragon,
            "victory": self.scene_victory,
            "defeat": self.scene_defeat,
        }
        self.current_scene: str = "intro"

    def run(self) -> None:
        """Run the main game loop."""
        utils.clear_screen()
        print(scenarios.INTRO_ART)
        utils.print_divider()
        print("중세 왕국의 용사를 위한 모험이 지금 시작됩니다!")
        utils.print_divider()

        name = input("당신의 이름은 무엇입니까, 용사여? ").strip() or "이름 없는 용사"
        self.player = Player(name=name)
        utils.prompt_continue()

        while self.player.is_alive() and self.current_scene:
            handler = self.scenes.get(self.current_scene)
            if handler is None:
                print(f"알 수 없는 장면으로 이동하려 했습니다: {self.current_scene}")
                break
            next_scene = handler()
            if next_scene is None:
                break
            self.current_scene = next_scene

        if not self.player.is_alive():
            self.scene_defeat()

    # Scene definitions -------------------------------------------------

    def scene_intro(self) -> Optional[str]:
        assert self.player is not None
        utils.clear_screen()
        utils.print_divider()
        print(f"{self.player.name} 님, 당신은 용맹한 기사단의 견습생입니다.")
        print("마을 광장에서 북쪽 고성에서 연기가 피어오르는 것을 보았습니다.")
        utils.print_divider()
        return utils.prompt_choice(
            "어디로 향하시겠습니까?",
            [
                ("마을 장로에게 상황을 묻는다.", "council"),
                ("시장으로 가서 대비한다.", "market"),
            ],
        )

    def scene_council(self) -> Optional[str]:
        assert self.player is not None
        utils.clear_screen()
        utils.print_divider()
        print("장로 드라몬드는 당신을 맞이하며 낮은 목소리로 속삭입니다.")
        print(scenarios.ELDER_PROPHECY)
        utils.print_divider()
        choice = utils.prompt_choice(
            "장로의 부탁을 어떻게 하시겠습니까?",
            [
                ("사명을 받아들여 숲으로 향한다.", "forest"),
                ("용과의 대결을 포기하고 집으로 돌아간다.", "defeat"),
            ],
        )
        if choice == "forest":
            print("장로는 당신에게 낡았지만 믿음직한 방패를 건네줍니다.")
            self.player.add_item("장로의 방패")
            utils.prompt_continue()
        return choice

    def scene_market(self) -> Optional[str]:
        assert self.player is not None
        utils.clear_screen()
        utils.print_divider()
        print("시장 상인들은 분주하지만 당신을 알아보고 도움을 청합니다.")
        print("약초상은 비밀스러운 미소를 지으며 물약을 내밉니다.")
        utils.print_divider()

        options = [("약초상에게서 치유 물약을 3골드에 산다.", "buy"), ("돈을 아끼고 떠난다.", "leave")]
        choice = utils.prompt_choice("어떻게 하시겠습니까?", options)
        if choice == "buy":
            if self.player.gold >= 3:
                self.player.gold -= 3
                self.player.add_item("치유 물약")
                print("따뜻한 빛이 감도는 병을 얻었습니다. 필요할 때 사용할 수 있을 것 같습니다.")
            else:
                print("골드가 부족합니다. 상인은 안타까운 듯 고개를 젓습니다.")
            utils.prompt_continue()
        return "intro"

    def scene_forest(self) -> Optional[str]:
        assert self.player is not None
        utils.clear_screen()
        utils.print_divider()
        print("북쪽 숲은 안개로 가득 차 있고, 먼 곳에서 북소리가 울립니다.")
        print("두 갈래 길이 나타났습니다. 하나는 반짝이는 빛이 비추고, 다른 하나는 발자국이 많습니다.")
        utils.print_divider()
        return utils.prompt_choice(
            "어느 길을 선택하시겠습니까?",
            [
                ("빛나는 길을 따른다.", "shrine"),
                ("발자국이 많은 길을 따른다.", "bandit"),
            ],
        )

    def scene_bandit(self) -> Optional[str]:
        assert self.player is not None
        utils.clear_screen()
        utils.print_divider()
        print("숲의 그늘 속에서 무장한 산적들이 나타납니다!")
        print(scenarios.BANDIT_TAUNT)
        utils.print_divider()
        if self.player.has_item("장로의 방패"):
            print("당신은 방패로 공격을 막고 빠르게 반격합니다.")
            print("산적들은 물러나며 주머니에 있던 4골드를 떨어뜨립니다.")
            self.player.gold += 4
        else:
            print("방패가 없어 산적의 칼날이 스쳐 지나갑니다!")
            self.player.take_damage(4)
            if self.player.is_alive():
                print(f"체력이 {self.player.health} 남았습니다.")
        utils.prompt_continue()
        if not self.player.is_alive():
            return "defeat"
        return "forest"

    def scene_shrine(self) -> Optional[str]:
        assert self.player is not None
        utils.clear_screen()
        utils.print_divider()
        print("고대의 숲 한가운데 작은 성소가 모습을 드러냅니다.")
        print("석상은 용맹한 이에게 축복을 내린다고 전해집니다.")
        utils.print_divider()

        if self.player.has_item("치유 물약"):
            choice = utils.prompt_choice(
                "성소에 어떻게 기도하시겠습니까?",
                [
                    ("물약을 제물로 바쳐 축복을 받는다.", "offer"),
                    ("조용히 기도만 드리고 떠난다.", "leave"),
                ],
            )
            if choice == "offer":
                self.player.inventory.remove("치유 물약")
                self.player.add_item("빛나는 검")
                print("성소에서 신비한 빛이 뿜어져 나오며 검이 손에 쥐어집니다.")
                self.player.heal(3)
                print("몸과 마음이 가벼워졌습니다! 체력이 3 회복됩니다.")
            else:
                print("성소는 조용히 빛나고 있을 뿐입니다.")
        else:
            print("적합한 제물이 없어 성소는 침묵을 지킵니다.")
            print("그러나 마음이 맑아져 체력이 1 회복되었습니다.")
            self.player.heal(1)
        utils.prompt_continue()
        return "ruins"

    def scene_ruins(self) -> Optional[str]:
        assert self.player is not None
        utils.clear_screen()
        utils.print_divider()
        print("고성의 폐허에 도착했습니다. 하늘에는 잿빛 구름이 드리워져 있습니다.")
        print("성문 앞에는 용을 숭배하던 자들의 흔적이 남아 있습니다.")
        utils.print_divider()
        choice = utils.prompt_choice(
            "마지막 준비를 어떻게 하시겠습니까?",
            [
                ("잔해 속을 뒤져 유용한 물건을 찾는다.", "scavenge"),
                ("바로 용의 둥지로 들어간다.", "dragon"),
            ],
        )
        if choice == "scavenge":
            print("당신은 무너진 성벽 사이를 뒤지다가 오래된 성배를 발견합니다!")
            self.player.add_item("성스러운 성배")
            utils.prompt_continue()
        return "dragon"

    def scene_dragon(self) -> Optional[str]:
        assert self.player is not None
        utils.clear_screen()
        utils.print_divider()
        print(scenarios.DRAGON_INTRO)
        utils.print_divider()

        if self.player.has_item("빛나는 검") and self.player.has_item("성스러운 성배"):
            print("검과 성배가 공명하며 용의 분노를 잠재우는 빛을 발합니다.")
            return "victory"

        if self.player.has_item("빛나는 검"):
            print("검이 용의 비늘을 꿰뚫지만, 분노한 용은 여전히 맹렬합니다.")
            if self.player.has_item("장로의 방패"):
                print("방패가 용의 불길을 막아내고, 겨우 도망칠 시간을 벌어줍니다.")
                self.player.take_damage(5)
            else:
                self.player.take_damage(8)
                print("화염이 당신을 덮칩니다!")
        elif self.player.has_item("성스러운 성배"):
            print("성배의 빛이 용을 잠시 진정시키지만, 무기가 없어 싸움을 끝내지 못합니다.")
            self.player.take_damage(6)
        else:
            print("준비되지 않은 당신은 용의 위용 앞에 압도됩니다.")
            self.player.take_damage(10)

        if self.player.is_alive():
            print("간신히 살아남았지만, 용은 여전히 성을 차지하고 있습니다.")
            utils.prompt_continue()
            return "defeat"
        return "defeat"

    def scene_victory(self) -> Optional[str]:
        assert self.player is not None
        utils.clear_screen()
        utils.print_divider()
        print("승리! 당신은 전설적인 영웅이 되었습니다.")
        print(scenarios.ENDING_SUCCESS)
        utils.print_divider()
        print(f"보유 골드: {self.player.gold}")
        print(f"획득한 아이템: {utils.format_inventory(self.player.inventory)}")
        utils.print_divider()
        return None

    def scene_defeat(self) -> Optional[str]:
        assert self.player is not None
        utils.print_divider()
        print("모험은 여기서 끝났습니다.")
        print(scenarios.ENDING_FAILURE)
        utils.print_divider()
        print(f"최종 체력: {self.player.health}")
        print(f"보유 골드: {self.player.gold}")
        utils.print_divider()
        return None
