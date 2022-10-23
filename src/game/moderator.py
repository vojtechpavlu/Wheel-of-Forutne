""""""
from src.game import Wedge
from src.game.game import AbstractGame
from src.player.abstract_player import Player


class Moderator:
    """"""

    def __init__(self, game: AbstractGame, quiet: bool = False):
        """"""
        self._game = game
        self._quiet = quiet

    @property
    def game(self) -> AbstractGame:
        """"""
        return self._game

    @property
    def quiet(self) -> bool:
        """"""
        return self._quiet

    def say(self, replica: str):
        """"""
        if not self.quiet:
            print(replica)

    def ask_for_letter(self, player: Player) -> str:
        """"""
        self.say(f"Tak jaké zkusíme další písmenko?")
        return player.guess_letter(
            self.game.guessed_letters, self.game.phrase.current_phrase)

    def handle_bankrupt(self, player: Player):
        """"""
        self.say(f"Bohužel hráč {player.player_name} nemá štěstí... "
                 f"Vytočil si políčko bankrot.")
        self.game.bankrupt_player(player)

    def handle_success_turn(self, wedge: Wedge, player: Player) -> bool:
        """"""
        self.say(f"Vytočili jste si krásné políčko {wedge.name}. "
                 f"Jaké zkusíme písmenko?")

        guess = self.ask_for_letter(player)

        occurrences = self.game.phrase.guess(guess)

        if occurrences > 0:
            prize = wedge.multiplier * occurrences
            self.game.increase_player_score(player, prize)
            print(f"Uhodl jste {occurrences} znaků a dostáváte {prize} bodů!")
            return True
        else:
            self.say(f"Bohužel znak '{guess}' v tajence není...")
            return False

    def do_the_turn(self):
        """"""
        player = self.game.current_player
        wedge = self.game.turn_the_wheel()

        # Pokud bankrot
        if wedge.is_bankrupt:
            self.handle_bankrupt(player)
            return

        # Hraje hráč znovu?
        another_turn = self.handle_success_turn(wedge, player)

        if not another_turn:
            self.game.set_next_player()

