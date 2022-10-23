
from src.game import default_wheel
from src.game.moderator import Moderator
from src.game.game import SinglePlayerGame
from src.player.human_player import HumanPlayer

phrase = "TO BE OR NOT TO BE"

wheel = default_wheel()
player = HumanPlayer("Karel")
game = SinglePlayerGame(phrase, wheel, player)
moderator = Moderator(game)

moderator.run_game()
