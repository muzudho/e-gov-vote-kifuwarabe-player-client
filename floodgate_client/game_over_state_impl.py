import time
from floodgate_client.transition_map_d.game_over import GameOverState


class GameOverStateImpl():
    def __init__(self):
        pass

    def create_game_over_state(self):
        """ステート生成"""
        state = GameOverState()

        return state
