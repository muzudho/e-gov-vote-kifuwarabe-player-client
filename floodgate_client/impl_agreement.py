from app import app
from floodgate_client.scripts.client_socket import client_socket
from floodgate_client.transition_map_d.agreement import AgreementState


def create_agreement_state():
    """ステート生成"""
    state = AgreementState()

    def on_entry(context):
        app.log.write_by_internal(
            f"[DEBUG] entry/[Agreement] (diagram.py 160)")
        # 常に AGREE を返します
        context.agree_func()

    state.on_entry = on_entry

    def on_exit(context):
        app.log.write_by_internal(
            f"[DEBUG] exit/[Agreement] (diagram.py 168) context.my_turn={context.my_turn} context.current_turn={context.current_turn}")
        if context.my_turn == context.current_turn:
            # 初手を考えます
            app.log.write_by_internal(
                f"(175) exit/[Agreement] で初手を考えます")
            m = context.go_func()
            client_socket.send_line(f'{m}\n')
            app.log.write_by_internal(
                f"(178) 初手を指します m=[{m}]")

    state.on_exit = on_exit

    return state
