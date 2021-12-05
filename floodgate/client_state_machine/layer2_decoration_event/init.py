from config import CLIENT_USER, CLIENT_PASS
from config import CLIENT_USER, CLIENT_PASS
from app import app
from floodgate_client_state.layer1_transition_map.init import InitState


def create():
    """ステート生成"""
    return DecoratedInitState()


class DecoratedInitState(InitState):
    def __init__(self):
        super().__init__()

    def on_entry(self, context):
        app.log.write_by_internal('on_entry しました (decoration/init.py 15)')

        # ログを初期状態に戻します
        app.log.init()
        app.log.write_by_internal(
            f"初期状態に戻します (entry/[Init])")

        # 通信ソケットを初期状態に戻し、接続を行います
        context.client_socket.set_up()
        context.client_socket.connect()

    def on_login(self, context):
        app.log.write_by_internal(
            'on_login しました (decoration/init.py 27)')

        # ログインコマンドを送信します
        command = f"LOGIN {CLIENT_USER} {CLIENT_PASS}\n"
        context.client_socket.send_line(command)