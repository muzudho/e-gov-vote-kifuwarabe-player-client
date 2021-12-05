from app import app
from floodgate.client_state_machine.layer1_transition_map.game import _TransitionState
from floodgate.client_state_machine.layer2_decoration_event.clean_up_vote import clean_up_vote
# from my_dynamodb.delete_table_bestmove import delete_bestmove_table
# from my_dynamodb.create_table_bestmove import create_bestmove_table


def create():
    """ステート生成"""
    return _DecoratedState()


class _DecoratedState(_TransitionState):

    def __init__(self):
        super().__init__()

    def on_move(self, req):
        """ここでサーバーへ指し手を送信してください"""
        # 相手の指し手だったら、自分の指し手を入力する番になります
        if req.context.current_turn != req.context.my_turn:
            app.log.write_by_internal(
                f"自分の手番が回ってきました。考えます: current_turn=[{req.context.current_turn}] my_turn=[{req.context.my_turn}]")
            m = req.context.go_func()
            req.context.client_socket.send_line(f'{m}\n')
            app.log.write_by_internal(
                f"(191) 自分の手番で指した m=[{m}]")

        clean_up_vote(req.context)

        # 盤表示
        text = req.context.position.formatBoard()
        app.log.write_by_internal(text)

    def on_move_echo(self, req):
        pass

    def on_game_over(self, req):
        pass

    def on_floodgate(self, req):
        pass

    def on_wcsc(self, req):
        pass
