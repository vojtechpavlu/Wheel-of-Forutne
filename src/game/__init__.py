""""""
from src.game.wheel import Wedge, Wheel


def create_wedge(multiplier: int) -> Wedge:
    """Pomocná funkce, která vygeneruje výherní klín pro dodaný multiplikátor.
    """
    return Wedge(f"${multiplier}", multiplier)


def create_bankrupt_wedge() -> Wedge:
    """Pomocná funkce, která vygeneruje klín bankrotu."""
    return Wedge(Wedge.BANKRUPT_NAME, 0)


def default_wedges() -> Wheel:
    """Funkce vrací výchozí stavbu kola, které obsahuje základní výherní klíny.
    """
    return Wheel(
        (
            # 21 výherních klínů
            create_wedge(800), create_wedge(500), create_wedge(650),
            create_wedge(500), create_wedge(500), create_wedge(900),
            create_wedge(700), create_wedge(600), create_wedge(800),
            create_wedge(500), create_wedge(700), create_wedge(500),
            create_wedge(600), create_wedge(550), create_wedge(500),
            create_wedge(900), create_wedge(650), create_wedge(900),
            create_wedge(900), create_wedge(300), create_wedge(700),

            # Dva klíny bankrotu
            create_bankrupt_wedge(), create_bankrupt_wedge(),
        ))
