from config import CLIENT_USER, CLIENT_PASS
from config import CLIENT_USER, CLIENT_PASS
from app import app
from floodgate.client_state_machine.layer1_transition_map.init import _TransitionState


def create():
    """ステート生成"""
    return _DecoratedState()


class _DecoratedState(_TransitionState):
    def __init__(self):
        super().__init__()

    def on_entry(self, req):
        app.log.write_by_internal('on_entry しました (decoration/init.py 15)')

        # ログを初期状態に戻します
        app.log.init()
        app.log.write_by_internal(
            f"初期状態に戻します (entry/[Init])")

        # 通信ソケットを初期状態に戻し、接続を行います
        req.context.client_socket.set_up()
        req.context.client_socket.connect()

    def on_login(self, req):
        app.log.write_by_internal(
            'on_login しました (decoration/init.py 27)')

        # ログインコマンドを送信します
        command = f"LOGIN {CLIENT_USER} {CLIENT_PASS}\n"
        req.context.client_socket.send_line(command)

    def on_login(self, req):
        pass

    def on_ok(self, req):
        pass

    def on_incorrect(self, req):
        pass
