from floodgate_client.transition_map_d.none import NoneState


def create_none_state():
    """ステート生成"""
    state = NoneState()

    def on_ok(_context):
        pass

    state.on_ok = on_ok
    return state
