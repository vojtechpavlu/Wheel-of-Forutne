""""""

import unicodedata


class Letter:
    """Instance této třídy reprezentují funkční obal znaku tajenky."""

    # Zástupný znak pro doposud neodhalené písmeno tajenky
    WILDCARD = "_"

    def __init__(self, letter: str, is_special: bool = False):
        """Initor, který přijímá znak, který má tajenka obsahovat. Dále je
        volitelným parametrem booleovský `is_special`, který umožňuje
        specifikovat speciální znaky, které jsou automaticky považovány
        za odhalené.

        Pokud je jako argument postoupen do parametru `letter` textový
        řetězec o délce jiné než 1, je vyhozena `ValueError`.
        """
        # Pokud písmeno není právě jedním znakem
        if len(letter) != 1:
            raise ValueError(f"Povolen je pouze právě jeden znak: '{letter}'!")

        # Skutečně privátní proměnná
        self.__letter = letter.upper()
        self._is_special = is_special
        self._is_revealed = is_special

    @property
    def letter(self) -> str:
        """Znak, kterému tato instance v aktuální pozici odpovídá. To znamená,
        že bylo-li doposud odhaleno, vrací svůj skutečný vnitřní znak, jinak
        vrací znak zástupný.
        """
        return self.__letter if self.is_revealed else self.WILDCARD

    @property
    def is_revealed(self) -> bool:
        """Reprezentuje, zda-li znak byl či nebyl uhodnut."""
        return self._is_revealed

    @property
    def is_special(self) -> bool:
        """Je-li znak speciální či nikoliv."""
        return self._is_special

    def guess(self, letter: str) -> bool:
        """Funkce, která ověří, zda-li bylo písmeno uhodnuto.

        Pokud tento dodaný znak (`letter`) odpovídá znaku, který tato instance
        zastává a zároveň doposud nebyl znak uhodnut, pak nastaví svůj stav
        uhodnutí na True a True také vrací. Pokud nebylo doposud odhaleno a
        dodané písmeno neodpovídá vnitnřímu stavu, je pouze vrácena hodnota
        False.

        Funkce vyhazuje výjimku, pokud je dodán textový řetězec o délce jiné,
        než je právě jeden znak.
        """
        if len(letter) != 1:
            raise ValueError(f"Povolen je právě jeden znak: '{letter}'!")

        letter = self.process(letter)

        if letter == self.process(self.__letter) and not self.is_revealed:
            self._is_revealed = True
            return True
        return False

    @staticmethod
    def process(letter: str) -> str:
        """Upraví textový řetězec tak, aby se dal porovnat nezávisle na
        velikosti písmen ani na diakritice.
        """
        return remove_accents(letter).upper()


class SecretPhrase:
    """Instance této třídy reprezentují tajenku, která má být uhodnuta.
    Samotná tajenka se sestává z písmen, která jsou obalena instancemi třídy
    Letter."""

    # Speciální znaky, které se nehádají
    SPECIAL_CHARACTERS = [" ", '"', "'", ",", "-", ".", "!", "?"]

    def __init__(self, phrase: str):
        """Initor, který přijímá tajnou frázi (tajenku) k uhodnutí.
        Ta musí být neprázdná, jinak je vyhozena výjimka."""

        if len(phrase) == 0:
            raise ValueError(f"Tajenka musí být neprázdná!")

        self.__phrase = phrase
        self.__letters = []

        # Pro každé jedno písmeno v dodané tajence
        for letter in list(phrase):
            self.__letters.append(
                Letter(letter, letter in self.SPECIAL_CHARACTERS))

    @property
    def current_phrase(self) -> str:
        """Aktuální podoba hádánky se zakrytými neuhodnutými písmeny."""
        phrase = ""
        for letter in self.__letters:
            phrase += letter.letter
        return phrase

    @property
    def phrase_len(self) -> int:
        """Délka celé tajenky."""
        return len(self.__phrase)

    @property
    def revealed_characters(self) -> tuple[Letter]:
        """Všechny odkryté znaky."""
        return tuple(filter(lambda ltr: ltr.is_revealed, self.__letters))

    @property
    def special_characters(self) -> tuple[Letter]:
        """Všechny speciální znaky tajenky."""
        return tuple(filter(lambda ltr: ltr.is_special, self.__letters))

    def guess(self, letter: str) -> int:
        """Funkce, která vrací počet nalezených výskytů daného písmene v
        tajence. Pokud dodaný počet znaků odhadovaného řetězce není roven 1,
        je vyhozena výjimka.
        """
        if len(letter) != 1:
            raise ValueError(f"Povolen je právě jeden znak: '{letter}'!")

        return len([ltr for ltr in self.__letters if ltr.guess(letter)])


def remove_accents(string_with_accents: str) -> str:
    """Funkce odpovědná za odstranění diakritiky."""
    return str(
        unicodedata.normalize("NFD", string_with_accents)
        .encode("ascii", "ignore")
        .decode("utf-8"))
