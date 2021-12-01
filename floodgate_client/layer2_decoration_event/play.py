import time
from app import app
from floodgate_client.layer1_transition_map.play import PlayState
from my_dynamodb.delete_table_bestmove import delete_bestmove_table
from my_dynamodb.create_table_bestmove import create_bestmove_table


def create():
    """ステート生成"""
    return DecoratedPlayState()


class DecoratedPlayState(PlayState):
    def __init__(self):
        super().__init__()

    def on_move(self, context):
        """指し手"""
        # 相手の指し手だったら、自分の指し手を入力する番になります
        if context.current_turn != context.my_turn:
            app.log.write_by_internal(
                f"自分の手番が回ってきました。考えます: current_turn=[{context.current_turn}] my_turn=[{context.my_turn}]")
            m = context.go_func()
            context.client_socket.send_line(f'{m}\n')
            app.log.write_by_internal(
                f"(191) 自分の手番で指した m=[{m}]")

        # テーブルを削除します
        try:
            delete_bestmove_table()

            # 時間間隔を開けてみる
            time.sleep(5)
        except Exception as e:
            app.log.write_by_internal(
                f"(Err.178) テーブル削除できなかった [{e}]")
        # テーブルを作成します
        try:
            create_bestmove_table()

            # 時間間隔を開けてみる
            time.sleep(5)
        except Exception as e:
            app.log.write_by_internal(
                f"(Err.183) テーブル作成できなかった [{e}]")

        # 盤表示
        text = context.position.formatBoard()
        app.log.write_by_internal(text)

    def on_win(self, context):
        """勝ち"""
        s = f"""+----------+
|    WIN   |
+----------+
"""
        app.log.write_by_internal(s)

    def on_lose(self, context):
        """負け"""
        s = f"""+----------+
|   LOSE   |
+----------+
"""
        app.log.write_by_internal(s)