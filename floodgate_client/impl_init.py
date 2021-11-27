from floodgate_client.transition_map_d.init import InitState


def create_init_state():
    """ステート生成"""
    state = InitState()

    def on_ok(_context):
        pass

    state.on_ok = on_ok
    return state
