""""""


from abc import ABC, abstractmethod

from src.game.game import AbstractGame


class Player(ABC):
    """"""

    def __init__(self):
        """"""

    @property
    @abstractmethod
    def score(self) -> int:
        """"""

    @score.setter
    @abstractmethod
    def score(self, new_score) -> int:
        """"""

    @abstractmethod
    def guess_letter(self, game: AbstractGame) -> str:
        """"""


