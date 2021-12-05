from app import app
from floodgate.client_state_machine.layer1_transition_map.reply import _TransitionState
from floodgate.client_state_machine.layer2_decoration_event.clean_up_vote import clean_up_vote


def create():
    """ステート生成"""
    return _DecoratedState()


class _DecoratedState(_TransitionState):
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

    def on_agree(self, req):
        """対局条件を読み終わったところでAgreeします"""
        app.log.write_by_internal(
            f"[DEBUG] [Listen]on_agree (listen.py 17)")
        # 常に AGREE を返します
        req.context.agree_func()

    def on_start(self, req):
        """自分の手番へ"""
        clean_up_vote(req)

        if req.context.my_turn == req.context.current_turn:
            # TODO 自分の手番なら、初手を考えます
            pass
        else:
            pass

    def on_reject_c(self, req):
        pass

    def on_reject_s(self, req):
        pass
