from floodgate_client.layer1_transition_map.listen import ListenState
from floodgate_client.layer2_decoration_event.clean_up_vote import clean_up_vote


def create():
    """ステート生成"""
    return DecoratedListenState()


class DecoratedListenState(ListenState):
    def __init__(self):
        super().__init__()

    def on_start_me(self, context):
        """自分の手番へ"""
        clean_up_vote(context)

    def on_start_you(self, context):
        """相手の手番へ"""
        clean_up_vote(context)
