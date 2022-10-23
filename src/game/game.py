""""""
from typing import Iterable
from abc import ABC, abstractmethod

from src.game.phrase import SecretPhrase
from src.game.wheel import Wheel
from src.player.abstract_player import Player


class AbstractGame(ABC):
    """"""

    def __init__(self, phrase: str, wheel: Wheel, players: Iterable[Player]):
        """"""
        self._wheel = wheel
        self._phrase = SecretPhrase(phrase)
        self._players = list(players)
        self.__guessed_letters: list[str] = []

    @property
    def wheel(self) -> Wheel:
        """Kolo štěstí, se kterým se v této hře hraje."""
        return self._wheel

    @property
    def players(self) -> tuple[Player]:
        """N-tice hráčů, kteří se této hry účastní."""
        return tuple(self._players)

    @property
    def number_of_players(self) -> int:
        """Počet hráčů v této hře."""
        return len(self.players)

    @property
    def phrase(self) -> SecretPhrase:
        """Tajenka, se kterou je v této hře cílem uhodnout."""
        return self._phrase

    @property
    def guessed_letters(self) -> tuple[str]:
        """N-tice již zkoušených písmen."""
        return tuple(self.__guessed_letters)

    @property
    @abstractmethod
    def current_player(self) -> Player:
        """Abstraktní vlastnost, která vrací dalšího hráče v pořadí."""

    def save_guess(self, guessed_letter: str):
        """Metoda, která uloží další pokus o uhodnutí znaku."""
        self.__guessed_letters.append(guessed_letter)

    @abstractmethod
    def set_next_player(self):
        """Abstraktní metoda, která nastaví dalšího hráče v pořadí jako
        aktuálního hráče."""

    def turn(self):
        """"""
        wedge = self.wheel.rotate()
        player = self.current_player

        # Pokud je políčko BANKROT, vynuluj hráči jeho skóre
        if wedge.is_bankrupt:
            player.score = 0
        else:
            # Zvyš skóre hráče o výhru násobenou výskyty písmene v tajence
            guessed_letter = player.guess_letter(self)
            occurrences = self.phrase.guess(guessed_letter)
            player.score += wedge.multiplier * occurrences
        self.set_next_player()


class MultiplayerGame(AbstractGame):
    """Instance hry, která je určena pro více hráčů."""

    def __init__(self, phrase: str, wheel: Wheel, players: Iterable[Player]):
        """"""
        super().__init__(phrase, wheel, players)

        if len(self.players) > 5:
            raise ValueError(f"Počet hráčů < 2: {len(self.players)}")

        # Index prvního hráče - ve výchozí pozici nastaveno na 0
        self.__current_player_idx = 0

    @property
    def current_player(self) -> Player:
        """Aktuální hráč, který je právě na tahu."""
        return self.players[self.__current_player_idx]

    def set_next_player(self):
        """Metoda, která se postará o nastavení dalšího hráče na tahu.
        Pokud je aktuální hráč posledním, kruhem se přesune tah opět na
        toho prvního.
        """
        # Pokud je hráč posledním v řadě, další je opět první
        if (self.number_of_players - 1) == self.__current_player_idx:
            self.__current_player_idx = 0

        # Jinak je nastaven aktuální hráč na dalšího v pořadí
        else:
            self.__current_player_idx += 1


class SinglePlayerGame(AbstractGame):
    """Instance hry, která je určena pro jediného hráče."""

    def __init__(self, phrase: str, wheel: Wheel, player: Player):
        """"""
        super().__init__(phrase, wheel, [player])

    @property
    def current_player(self) -> Player:
        """Aktuální hráč, který je právě na tahu. V případě hry pro jediného
        hráče pouze vrací právě toho."""
        return self.players[0]

    def set_next_player(self):
        """Pro hru jediného hráče je tato metoda redundantní."""
        ...

