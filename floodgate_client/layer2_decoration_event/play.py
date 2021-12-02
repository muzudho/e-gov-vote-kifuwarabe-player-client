import time
from app import app
from my_dynamodb.delete_table_bestmove import delete_bestmove_table
from my_dynamodb.create_table_bestmove import create_bestmove_table
from floodgate_client.layer1_transition_map.play import PlayState
from floodgate_client.layer2_decoration_event.clean_up_vote import clean_up_vote


def create():
    """ステート生成"""
    return DecoratedPlayState()


class DecoratedPlayState(PlayState):
    def __init__(self):
        super().__init__()

    def on_do_move(context):
        """ここでサーバーへ指し手を送信してください"""
        # 相手の指し手だったら、自分の指し手を入力する番になります
        if context.current_turn != context.my_turn:
            app.log.write_by_internal(
                f"自分の手番が回ってきました。考えます: current_turn=[{context.current_turn}] my_turn=[{context.my_turn}]")
            m = context.go_func()
            context.client_socket.send_line(f'{m}\n')
            app.log.write_by_internal(
                f"(191) 自分の手番で指した m=[{m}]")

        clean_up_vote(context)

        # 盤表示
        text = context.position.formatBoard()
        app.log.write_by_internal(text)
