
from src.game import default_wheel, wheel_without_bankrupts
from src.game.moderator import Moderator
from src.game.game import SinglePlayerGame, MultiplayerGame
from src.player.entropy_driven_player import (
    EntropyDrivenPlayerCZ, EntropyDrivenPlayerEN)
from src.player.human_player import HumanPlayer

phrase = "Poslušně hlásím, že jsem zase tady."
wheel = default_wheel()
players = [HumanPlayer("Já"), EntropyDrivenPlayerCZ()]
game = MultiplayerGame(phrase, wheel, players)
moderator = Moderator(game, True)

moderator.run_game()
