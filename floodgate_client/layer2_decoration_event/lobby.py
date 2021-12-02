from floodgate_client.layer1_transition_map.lobby import LobbyState


def create():
    """ステート生成"""
    return DecoratedLobbyState()


class DecoratedLobbyState(LobbyState):
    def __init__(self):
        super().__init__()
