from config import CLIENT_USER, CLIENT_PASS
from app import app
from floodgate_client.transition_map_d.init import InitState


def create_init_state():
    """ステート生成"""
    state = InitState()

    def __on_entry(context):
        # ログを初期状態に戻します
        app.log.init()
        app.log.write_by_internal(
            f"初期状態に戻します (diagram.py 66)")

        # 通信ソケットを初期状態に戻し、接続を行います
        context.client_socket.set_up()
        context.client_socket.connect()

        # ログインコマンドを送信します
        context.client_socket.send_line(
            f"LOGIN {CLIENT_USER} {CLIENT_PASS}\n")

    state.on_entry = __on_entry

    def __on_ok(_context):
        pass

    state.on_ok = __on_ok
    return state
