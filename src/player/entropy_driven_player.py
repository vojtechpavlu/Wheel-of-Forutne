""""""
from typing import Iterable

from src.player.abstract_player import AbstractPlayer


class EntropyDrivenPlayer(AbstractPlayer):
    """"""

    def __init__(self, player_name: str, relative_occurrence: str):
        super().__init__(player_name)
        self._relative_occurrence = relative_occurrence

    @property
    def relative_occurrence(self) -> tuple[str]:
        """"""
        return tuple(self._relative_occurrence)

    def guess_letter(self, already_guessed: Iterable[str], phrase: str) -> str:
        """"""
        for character in self.relative_occurrence:
            if character not in already_guessed:
                return character


class EntropyDrivenPlayerEN(EntropyDrivenPlayer):
    """"""

    def __init__(self):
        super().__init__(
            "ENGLISH ENTROPY-DRIVEN NPC", "ETAOINSHRDLCUMWFGYPBVKJXQZ")


class EntropyDrivenPlayerCZ(EntropyDrivenPlayer):
    """"""

    def __init__(self):
        super().__init__(
            "CZECH ENTROPY-DRIVEN NPC", "OENATVSILKRDPMUZJYCBHFGXWQ")


