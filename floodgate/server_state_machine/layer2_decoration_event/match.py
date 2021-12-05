from floodgate.server_state_machine.layer1_transition_map.match import MatchState


def create():
    """ステート生成"""
    return DecoratedMatchState()


class DecoratedMatchState(MatchState):
    def __init__(self):
        super().__init__()
