"""Modul obsahuje definici kola štěstí.

Kolo štěstí je souborem výherních klínů (instancí třídy `Wedge`). Tyto klíny
se setávají ze svého názvu a z multiplikátoru výhry. Mezi nimi může být i
klín BANKRUPT, který značí prohru.

Kolo štěstí poskytuje službu náhodného výběru takového klínu (simulace točení).
"""


from typing import Iterable
from random import choice


class Wedge:
    """Instance této třídy reprezentují výherní klíny. Ty slouží jako násobek
    původní výhry převedený na body.

    Kromě toho mohou tyto klíny nést i svoji textovou reprezentaci.

    Mezi výherními klíny jsou i takové, které hrají roli prohry, nazývají se
    bankrotové."""

    BANKRUPT_NAME = "BANKROT"

    def __init__(self, name: str, multiplier: int):
        """Initor, který přijímá název výherního klínu a násobek výhry.
        Pokud název odpovídá textovému řetězci v třídní proměnné
        `BANKRUPT_NAME`, je tento klín prohrou.
        """
        self._name = name
        self._multiplier = multiplier
        self._is_bankrupt = name == self.BANKRUPT_NAME

    @property
    def name(self) -> str:
        """Název klínu kola."""
        return self._name

    @property
    def multiplier(self) -> int:
        """Multiplikátor, kterým se násobí výhra."""
        return self._multiplier

    @property
    def is_bankrupt(self) -> bool:
        """Jestli je tento výherní klín bankrotem."""
        return self._is_bankrupt

    def __repr__(self) -> str:
        """Textová reprezentace výherního klínu."""
        return self.name


class Wheel:
    """Instance této třídy slouží jako kolo štěstí, které se sestává z
    výherních klínů. Kolo štěstí simuluje jeho zatočení a vrací náhodný
    výherní klín."""

    def __init__(self, wedges: Iterable[Wedge]):
        """Initor, který přijímá sadu klínů, ze kterých se kolo sestává.
        Z nich pak umožňuje na požádání náhodně vybrat jeden výherní klín.
        """
        self._wedges = list(wedges)

    @property
    def wedges(self) -> tuple[Wedge]:
        """Všechny výherní klíny, které byly kolu dodány."""
        return tuple(self._wedges)

    def rotate(self) -> Wedge:
        """Simulace točení kola štěstí. Metoda náhodně vybere jeden klín,
        který vrací."""
        return choice(self.wedges)
