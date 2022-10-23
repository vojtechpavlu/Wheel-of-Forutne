"""Tento modul obsahuje prostředky pro práci s tajenkou.

Obsahuje především definici třídy `SecretPhrase`, která má za cíl poskytovat
službu správy tajenky. Ta se sestává ze znaků, které mají být uhodnuty.

Těmito znaky jsou instance třídy `Letter`, která obsalují jednotlivá písmena
tajenky a udržují si informaci o tom, zda-li byly již uhodnuty či třeba zda-li
nejde o speciální znak (např. interpunkční znaménka), který je defaultně
odkryt."""

# Import knihovny pro práci se znaky s diakritikou
import unicodedata


class Letter:
    """Instance této třídy reprezentují funkční obal znaku tajenky.
    Coby obal se v tomto kontextu chová jako bezpečnostní mechanismus, který
    daný znak ukrývá svým zástupným znakem (viz třídní proměnná `WILDCARD`),
    aby nebylo vyzrazeno, ale bylo nutné ho uhodnout. Po uhodnutí již tyto
    instance svůj znak nijak neskrývají.

    Speciálním případem jsou speciální znaky (typicky interpunkční znaménka),
    která ze své podstaty nemá smysl hádat, proto jsou ve výchozím stavu již
    od počátku odhalena.

    Díky tomuto mechanismu je možné, aby byla tajenka snadno ukázána a přitom
    se mohly jednotlivá písmena rozhodnout na základě svého uhodnutí, zda-li
    se odkryjí či vrátí za sebe zástupný znak."""

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
    Letter.

    Na základě dodané hádané tajenky si tato instance vybuduje posloupnost
    takto obalených znaků, které se skrývají do té doby, dokud nejsou uhodnuty.

    Tajenka umí na základě dodaného hádaného znaku říci, kolikrát se v tajence
    vyskytuje (na základě čehož jsou počítány body) a příslušným znakům
    přenechá odpovědnost za své další skrývání či odkrývání.

    Tajenka se rozhoduje na počátku, které znaky budou od začátku odkryty a
    které naopak schová - speciální znaky (např. interpunkční znaménka) nemá
    smysl skrývat, celý seznam takovýchto znaků lze vidět v třídní proměnné
    `SPECIAL_CHARACTERS`."""

    # Speciální znaky, které se nehádají
    SPECIAL_CHARACTERS = [" ", '"', "'", ",", "-", ".", "!", "?"]

    def __init__(self, phrase: str):
        """Initor, který přijímá tajnou frázi (tajenku) k uhodnutí.
        Ta musí být neprázdná, jinak je vyhozena výjimka.

        Kromě testu validity initor odpovídá za vybudování ochranných obalů
        pro jednotlivá písmena. Ten tvoří rozdělením tajenky na jednotlivé
        znaky, které poté obaluje instancemi třídy `Letter`. Speciální znaky
        pak postupuje s příslušnou informací, díky čemuž zůstávají neskrývané
        už od začátku."""

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
    """Funkce odpovědná za odstranění diakritiky. Díky tomu je možné odhalovat
    i písmena, která jsou s diakritikou pomocí pokusů se znaky, které takto
    opatřeny nejsou.

    Například v tajence 'ŘEŘICHA' by pomocí pokusu s písmenem 'R' byly oba
    výskyty 'Ř' správně odhaleny.
    """
    return str(
        unicodedata.normalize("NFD", string_with_accents)
        .encode("ascii", "ignore")
        .decode("utf-8"))
