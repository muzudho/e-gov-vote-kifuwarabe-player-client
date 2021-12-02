from app import app
from floodgate_client.layer1_transition_map.entrance import EntranceState


def create():
    """ステート生成"""
    return DecoratedEntranceState()


class DecoratedEntranceState(EntranceState):
    def __init__(self):
        super().__init__()
