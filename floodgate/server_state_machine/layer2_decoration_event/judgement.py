import time
from app import app
from floodgate.server_state_machine.layer1_transition_map.judgement import _TransitionState
# from my_dynamodb.delete_table_bestmove import delete_bestmove_table
# from my_dynamodb.create_table_bestmove import create_bestmove_table


def create():
    """ステート生成"""
    return _DecoratedState()


class _DecoratedState(_TransitionState):
    def __init__(self):
        super().__init__()

    def on_move(self, req):
        pass

    def on_move_echo(self, req):
        pass

    def on_game_over(self, req):
        pass

    def on_floodgate(self, req):
        pass

    def on_wcsc(self, req):
        pass

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
