"""Tento modul obsahuje definici hry.

Jako hru lze chápat prostředek, pomocí kterého lze řídit průběh hry, co do
řízení tahů hráčů, tak i co do stavu hry jako takové.

Obecně lze chápat v kontextu tohoto typu hry dva základní módy:

- Multiplayer mód, kde hraje více hráčů proti sobě
- Singleplayer mód, kde hraje jediný hráč (hra pak odpovídá spíše hře
  'Hangman', oběšenec).

Oba tyto módy mají mnoho společných znaků, které jsou sdruženy do společného
abstraktního předka `AbstractGame`.
"""

from typing import Iterable
from abc import ABC, abstractmethod

from src.game.phrase import SecretPhrase
from src.game.wheel import Wheel, Wedge
from src.player.abstract_player import Player


class AbstractGame(ABC):
    """Abstraktní typ hry, který sdružuje společnou funkcionalitu obou módů
    hry (SinglePlayer a MultiPlayer).

    Instance této třídy jsou odpovědné za sdružování prostředků pro hru
    (kolo štěstí, tajneku a hráče) a poskytuje protokol pro řízení průběhu
    celé hry.
    """

    def __init__(self, phrase: str, wheel: Wheel, players: Iterable[Player]):
        """Initor, který přijímá tajenku (v prostém textovém řetězci),
        vybudované kolo štěstí (pomocí kterého lze určovat ceny za uhodnutý
        znak tajenky) a sadu hráčů (kteří mohou tuto hru hrát a jsou dotazováni
        během svého tahu na svůj pokus o uhodnutí dalšího písmene hádanky).
        """
        self._wheel = wheel
        self._phrase = SecretPhrase(phrase)
        self.__guessed_letters: list[str] = []

        # Pro každého hráče ulož hráče jako n-tici (hráč, skóre),
        # přičemž skóre je na počátku pochopitelně 0
        self._player_records = [(p, 0) for p in players]

    @property
    def wheel(self) -> Wheel:
        """Kolo štěstí, se kterým se v této hře hraje."""
        return self._wheel

    @property
    def players(self) -> tuple[Player]:
        """N-tice hráčů, kteří se této hry účastní."""
        return tuple([p[0] for p in self._player_records])

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

    def players_score(self, player: Player) -> int:
        """Metoda, která vrací skóre daného hráče."""
        for player_record in self._player_records:
            if player_record[0] == player:
                return player_record[1]
        raise Exception(f"Ve hře není hráč '{player}'")

    def set_player_score(self, player: Player, score: int):
        """Metoda, která nastavuje skóre daného hráče."""
        for index, player_record in enumerate(self._player_records):
            if player_record[0] == player:
                self._player_records[index] = (player, score)
        raise Exception(f"Ve hře není hráč '{player}'")

    def bankrupt_player(self, player: Player):
        """Metoda, která anuluje hráčovo skóre."""
        self.set_player_score(player, 0)

    def increase_player_score(self, player: Player, increment: int):
        """Metoda zvyšuje skóre daného hráče o dodaný přírustek."""
        self.set_player_score(player, self.players_score(player) + increment)

    @abstractmethod
    def set_next_player(self):
        """Abstraktní metoda, která nastaví dalšího hráče v pořadí jako
        aktuálního hráče."""

    def turn_the_wheel(self) -> Wedge:
        """Metoda, která řídí otočení kolem pro daný tah. Výsledný výherní
        klín je vrácen jako návratová hodnota."""
        return self.wheel.rotate()

    def turn(self):
        """"""
        wedge = self.wheel.rotate()
        player = self.current_player

        # Pokud je políčko BANKROT, vynuluj hráči jeho skóre
        if wedge.is_bankrupt:
            self.bankrupt_player(player)
        else:
            # Zvyš skóre hráče o výhru násobenou výskyty písmene v tajence
            guessed_letter = player.guess_letter(
                self.guessed_letters, self.phrase.current_phrase)

            # Počet uhodnutých výskytů hádaného písmene v hádance
            occurrences = self.phrase.guess(guessed_letter)

            # Zvýšení skóre hráče
            self.increase_player_score(player, wedge.multiplier * occurrences)

        # Nastavení dalšího hráče
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
        return self.players[self.__current_player_idx][0]

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
        return self.players[0][0]

    def set_next_player(self):
        """Pro hru jediného hráče je tato metoda redundantní."""
        ...

