from app import app
from floodgate_server_state.layer1_transition_map.receipt import EntranceState


def create():
    """ステート生成"""
    return DecoratedEntranceState()


class DecoratedEntranceState(EntranceState):
    def __init__(self):
        super().__init__()
