from app import app
from floodgate_client.transition_map_d.agreement import AgreementState


def create():
    """ステート生成"""
    return DecoratedAgreementState()


class DecoratedAgreementState(AgreementState):
    def __init__(self):
        super().__init__()

    def on_entry(self, context):
        app.log.write_by_internal(
            f"[DEBUG] entry/[Agreement] (diagram.py 160)")
        # 常に AGREE を返します
        context.agree_func()

    def on_exit(self, context):
        app.log.write_by_internal(
            f"[DEBUG] exit/[Agreement] (diagram.py 168) context.my_turn={context.my_turn} context.current_turn={context.current_turn}")
        if context.my_turn == context.current_turn:
            # 初手を考えます
            app.log.write_by_internal(
                f"(175) exit/[Agreement] で初手を考えます")
            m = context.go_func()
            context.client_socket.send_line(f'{m}\n')
            app.log.write_by_internal(
                f"(178) 初手を指します m=[{m}]")
