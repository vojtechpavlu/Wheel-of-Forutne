"""Tento modul obsahuje definici moderátora, coby nejvyšší řídící instituci
v rámci této hry.

Moderátor je odpovědný za řízení celé hry v kontextu dotazování se
jednotlivých hráčů na jejich tipy, stejně jako na přiřazování pořadí."""

from src.game import Wedge
from src.game.game import AbstractGame
from src.game.phrase import GuessError
from src.player.abstract_player import AbstractPlayer


class Moderator:
    """Instance této třídy jsou řídícím elementem celého systému. Řídí hru
    a celkově interagují s hráčem.
    """

    def __init__(self, game: AbstractGame, quiet: bool = False):
        """Initor, který přijímá instanci třídy `AbstractGame`, o kterou
        se má za úkol starat. Dále volitelný parametr `quiet`, který umožňuje
        moderátora 'umlčet', aby nevypisoval do konzole všechny repliky.
        """
        self._game = game
        self._quiet = quiet

    @property
    def game(self) -> AbstractGame:
        """Vrací referenci na hru, kterou tento moderátor řídí."""
        return self._game

    @property
    def quiet(self) -> bool:
        """Vrací, zda-li by měl moderátor mlčet či vypisovat do konzole."""
        return self._quiet

    def say(self, *replicas):
        """Metoda, pomocí které je možné řídít výřečnost moderátora. Pokud je
        nastavena instanční proměnná `quiet` na True, nebude zahlcovat konzoli
        všemi replikami. V opačném případě vypisuje všechny repliky.

        Metoda má význam pro testování."""
        if not self.quiet:
            print(*replicas)

    def introduce_game(self):
        """Metoda, pomocí které moderátor hru uvede."""
        self.say("Vítáme Vás u další hry Wheel of Fortune!")
        self.say(f"Dnes zde hraje {len(self.game.players)} hráčů:")
        for player in self.game.players:
            self.say("\t- ", player.player_name)
        print(f"Začněme tedy hádat tajenku: {self.game.phrase}")

    def end_game(self):
        """Metoda, kterou se moderátor rozloučí s hráči a hru ukončí.
        """
        print("Tajenka:", self.game.phrase)
        self.say("Konec hry. Dosažené skóre:")

        # Pro každého hráče vypiš dosažené skóre a pak poděkuj
        for p in self.game.players:
            print(f"\t{p.player_name}: {self.game.players_score(p)} bodů")
        self.say("Děkujeme, že jste si zahráli a příště naviděnou!")

    def ask_for_letter(self, player: AbstractPlayer) -> str:
        """Metoda, která se stará o vyzvání hráče k jeho dalšímu tipu písmene
        do tajenky."""
        self.say(f"Tak jaké zkusíme písmenko?")
        return player.guess_letter(
            self.game.guessed_letters, self.game.phrase.current_phrase)

    def turn_wheel(self) -> Wedge:
        """Metoda, která zatočí kolem štěstí. Vytočené políčko pak vrací."""
        return self.game.turn_the_wheel()

    def handle_bankrupt(self, player: AbstractPlayer):
        """Metoda, která má za cíl řídit průběh situace, kdy je hráči vytočeno
        políčko bankrotu. Pokud se tak stane, nemá nárok na žádné body (naopak
        jsou mu všechny strženy) a nemá nárok na další tah.
        """
        self.say(f"Bohužel hráč {player.player_name} nemá štěstí... "
                 f"Vytočil si políčko bankrot.")
        self.say("Přichází tak o všechny své body.")
        self.game.bankrupt_player(player)
        self.game.set_next_player()

    def player_guess(self, wedge: Wedge, player: AbstractPlayer) -> bool:
        """Metoda umožňující moderátorovi řídit průběh tahu jednoho hráče.
        Pokud uživatel úspěšně uhodne písmeno v tajence, měl by mít nárok na
        to, aby hrál znovu. V takovém případě metoda vrací True, jinak False.
        """

        """Iniciace řídících proměnných, kterých je použito pro ověření
        správnosti hráčova tahu."""
        occurrences = -1
        guess = ""

        """Opakuj, dokud uživatelův vstup není chybný, tedy dokud není
        počet výskytů dodaného písmena v tajence hráče větší nebo rovna 0."""
        while occurrences == -1:

            """Zeptej se hráče na jeho tip"""
            guess = self.ask_for_letter(player)

            """Vyzkoušej, zda-li uživatelův vstup není chybný (tedy který by
            tajenka nepřijala). Typicky jde o vstupy, které jsou víceznaké."""
            try:
                occurrences = self.game.phrase.guess(guess)
            except GuessError as ge:
                self.say(f"Pokus {ge.problem_letter} nelze použít... "
                         f"Zkuste to znovu!")

        """Ulož si vstup, který dále budeš poskytovat jako možnou nápovědu."""
        self.game.save_guess(guess)

        """Pokud bylo dodané písmeno v tajence, jsou uživateli přičteny body
        počítané jako násobek multiplikátoru políčka a počtu výskytů daného
        písmene v tajence. Zároveň má hráč nárok na další tah (vrací True)."""
        if occurrences > 0:
            prize = wedge.multiplier * occurrences
            self.game.increase_player_score(player, prize)
            self.say(f"Uhodl jste {occurrences} znaků v tajence a dostáváte "
                     f"{prize} bodů!")
            return True

        # Pokud v tajence tipované písmeno nebylo, žádné body hráč nedostává
        # a nemá nárok na další tah (vrací False)
        else:
            self.say(f"Bohužel písmeno '{guess}' v tajence není...")
            return False

    def do_the_turn(self):
        """Metoda, díky které moderátor řídí daný tah.
        V první řadě se zatočí kolem štěstí. Pokud padne BANKROT, je tah
        aktuálního hráče ukončen, jsou mu odečteny všechny body a dále hraje
        jeho následník.

        Pokud si nevytočí bankrot, je hráč dotázán na jeho tip na další
        písmeno v tajence. Pokud uhodne, jsou mu přičteny body a hraje znovu,
        v opačném případě hraje další hráč v pořadí.
        """
        player = self.game.current_player
        self.say(f"Na tahu je hráč '{player.player_name}'.")
        wedge = self.turn_wheel()

        # Pokud padne políčko bankrot
        if wedge.is_bankrupt:
            self.handle_bankrupt(player)
            return

        self.say(f"Vytočil jste si políčko {wedge.name}.")

        # Zeptej se uživatele; pokud neuhodl písmeno v tajence
        if not self.player_guess(wedge, player):
            self.game.set_next_player()

    def run_game(self):
        """Metoda starající se o celkový průběh hry.

        V první řadě hru moderátor uvítá. Dále opakuje (dokud není tajenka
        vyluštěna) jednotlivé tahy pro jednotlivé hráče.

        Jakmile je tajenka vyluštěna, je hra moderátorem ukončena.
        """
        # Uvítání
        self.introduce_game()

        # Dokud není tajenka vyluštěna
        while not self.game.phrase.is_finished:
            self.say(80*"-")
            self.do_the_turn()

        # Ukonči hru
        print(80*"-")
        self.end_game()


