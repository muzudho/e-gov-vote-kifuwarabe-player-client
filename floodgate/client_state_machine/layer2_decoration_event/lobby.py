from app import app
from floodgate.client_state_machine.layer1_transition_map.lobby import LobbyState


def create():
    """ステート生成"""
    return DecoratedLobbyState()


class DecoratedLobbyState(LobbyState):

    def __init__(self):
        super().__init__()

    def on_agree(self, context):
        """対局条件を読み終わったところでAgreeします"""
        app.log.write_by_internal(
            f"[DEBUG] [Listen]on_agree (listen.py 17)")
        # 常に AGREE を返します
        context.agree_func()
