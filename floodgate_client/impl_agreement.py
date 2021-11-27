from app import app
from floodgate_client.transition_map_d.agreement import AgreementState


def create_agreement_state():
    """ステート生成"""
    state = AgreementState()

    def __on_entry(context):
        app.log.write_by_internal(
            f"[DEBUG] entry/[Agreement] (diagram.py 160)")
        # 常に AGREE を返します
        context.agree_func()

    state.on_entry = __on_entry

    def __on_exit(context):
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

    state.on_exit = __on_exit

    return state
