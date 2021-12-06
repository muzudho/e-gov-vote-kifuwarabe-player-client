from app import app
from floodgate.server_state_machine.layer1_transition_map.receipt import ReceiptState as _TransitionState


def create():
    """ステート生成"""
    return _DecoratedState()


class _DecoratedState(_TransitionState):
    def __init__(self):
        super().__init__()
