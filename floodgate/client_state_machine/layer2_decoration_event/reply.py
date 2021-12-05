from app import app
from floodgate_client_state.layer1_transition_map.reply import ReplyState
from floodgate_client_state.layer2_decoration_event.clean_up_vote import clean_up_vote


def create():
    """ステート生成"""
    return DecoratedReplyState()


class DecoratedReplyState(ReplyState):
    def __init__(self):
        super().__init__()

    def on_exit(self, context):
        app.log.write_by_internal(
            f"[DEBUG] exit/[Reply] (diagram.py 168) context.my_turn={context.my_turn} context.current_turn={context.current_turn}")
        if context.my_turn == context.current_turn:
            # 初手を考えます
            app.log.write_by_internal(
                f"(175) exit/[Reply] で初手を考えます")
            m = context.go_func()
            context.client_socket.send_line(f'{m}\n')
            app.log.write_by_internal(
                f"(178) 初手を指します m=[{m}]")

    def on_start_me(self, context):
        """自分の手番へ"""
        clean_up_vote(context)

    def on_start_you(self, context):
        """相手の手番へ"""
        clean_up_vote(context)
