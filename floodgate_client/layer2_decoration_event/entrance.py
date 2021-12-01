from config import CLIENT_USER, CLIENT_PASS
from app import app
from floodgate_client.layer1_transition_map.entrance import EntranceState


def create():
    """ステート生成"""
    return DecoratedEntranceState()


class DecoratedEntranceState(EntranceState):
    def __init__(self):
        super().__init__()

    def on_entry(self, context):
        app.log.write_by_internal(
            'on_entry しました (decoration/entrance.py 17)')

        # ログインコマンドを送信します
        command = f"LOGIN {CLIENT_USER} {CLIENT_PASS}\n"
        context.client_socket.send_line(command)

    def on_ok(self, context):
        app.log.write_by_internal(
            'on_ok しました (decoration/entrance.py 25)')
        pass
