"""Tento modul obsahuje definici abstraktní třídy hráče, která je odpovědná
za sdružování společné funkcionality všech ostatních tříd hráčů a za
poskytování společné definice protokolu."""


from abc import ABC, abstractmethod
from typing import Iterable


class AbstractPlayer(ABC):
    """Abstraktní předek pro všechny hráče, který sdružuje společnou
    funkcionalitu a poskytuje společný zastřešující protokol pro všechny
    své potomky."""

    def __init__(self, player_name: str):
        """Initor, který přijímá pouze jméno daného hráče."""
        self._player_name = player_name

    @property
    def player_name(self) -> str:
        """Jméno hráče."""
        return self._player_name

    def __repr__(self):
        return self.player_name

    @abstractmethod
    def guess_letter(self, already_guessed: Iterable[str], phrase: str) -> str:
        """Abstraktní metoda, která definuje požadovanou signaturu pro každého
        hráče. Implementace této metody je odpovědná za pokus o uhodnutí
        dalšího písmene v tajence.

        K tomu dostává seznam písmen, která již byla použita, a z části
        skrytou tajenku, do které má za úkol další znak uhodnout.
        """


