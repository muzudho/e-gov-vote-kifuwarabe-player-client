from app import app
from floodgate.client_state_machine.layer1_transition_map.lobby import _TransitionState


def create():
    """ステート生成"""
    return _DecoratedState()


class _DecoratedState(_TransitionState):

    def __init__(self):
        super().__init__()

    def on_logout(self, req):
        pass

    def on_completed(self, req):
        pass

    def on_game_summary(self, req):
        pass
