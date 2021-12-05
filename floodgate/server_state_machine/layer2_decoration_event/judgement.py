import time
from app import app
from floodgate_client_state.layer1_transition_map.judge import JudgeState
from my_dynamodb.delete_table_bestmove import delete_bestmove_table
from my_dynamodb.create_table_bestmove import create_bestmove_table


def create():
    """ステート生成"""
    return DecoratedJudgeState()


class DecoratedJudgeState(JudgeState):
    def __init__(self):
        super().__init__()

    def on_win(self, context):
        """勝ち"""
        s = f"""
+----------+
|    WIN   |
+----------+
"""
        app.log.write_by_internal(s)

    def on_lose(self, context):
        """負け"""
        s = f"""
+----------+
|   LOSE   |
+----------+
"""
        app.log.write_by_internal(s)
