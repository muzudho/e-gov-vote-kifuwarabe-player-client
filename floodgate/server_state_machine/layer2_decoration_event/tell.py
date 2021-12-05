from app import app
from floodgate.server_state_machine.layer1_transition_map.tell import _TransitionState


def create():
    """ステート生成"""
    return _DecoratedState()


class _DecoratedState(_TransitionState):
    def __init__(self):
        super().__init__()

    def on_reject_c(self, req):
        pass

    def on_reject_s(self, req):
        pass

    def on_agree(self, req):
        pass

    def on_start(self, req):
        pass
