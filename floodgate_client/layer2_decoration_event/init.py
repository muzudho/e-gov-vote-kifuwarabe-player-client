from config import CLIENT_USER, CLIENT_PASS
from app import app
from floodgate_client.layer1_transition_map.init import InitState


def create():
    """ステート生成"""
    return DecoratedInitState()


class DecoratedInitState(InitState):
    def __init__(self):
        super().__init__()

    def on_entry(self, context):
        # ログを初期状態に戻します
        app.log.init()
        app.log.write_by_internal(
            f"初期状態に戻します (entry/[Init] behavior_init.py 14)")

        # 通信ソケットを初期状態に戻し、接続を行います
        context.client_socket.set_up()
        context.client_socket.connect()

        # ログインコマンドを送信します
        context.client_socket.send_line(
            f"LOGIN {CLIENT_USER} {CLIENT_PASS}\n")

    def on_ok(self, context):
        pass
