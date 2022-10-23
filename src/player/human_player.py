"""Tento modul obsahuje jednoduchou definici živého lidského uživatele.

Ten volí své tahy na základě člověkem zadaného vstupu.
"""

from typing import Iterable

from src.player.abstract_player import AbstractPlayer


class HumanPlayer(AbstractPlayer):
    """Instance této třídy reprezentují prostředníka, díky kterému je možné
    zapojit fyzického člověka do hry.

    Ten je vždy během jeho tahu vyzván, aby zadal svoji volbu odhadovaného
    písmene, přičemž je jeho úkolem toto zadat do konzole."""

    def __init__(self, player_name: str):
        """Initor, který přijímá pouze jméno hráče."""
        super().__init__(player_name)

    def guess_letter(self, already_guessed: Iterable[str], phrase: str) -> str:
        """Metoda, která je odpovědná za řízení sběru uživatelského vstupu.
        Ten je chápán jako tah ve hře.
        """
        print("Fráze k doplnění:", phrase)
        print("Již použitá písmena:", *already_guessed)
        return input("Zkuste uhodnout další písmeno: ").strip().upper()



