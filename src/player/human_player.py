""""""
from typing import Iterable

from src.player.abstract_player import AbstractPlayer


class HumanPlayer(AbstractPlayer):
    """"""

    def __init__(self, player_name: str):
        super().__init__(player_name)

    def guess_letter(self, already_guessed: Iterable[str], phrase: str) -> str:
        print("Fráze k doplnění:", phrase)
        return input("Zkuste uhodnout další písmeno: ").strip()



