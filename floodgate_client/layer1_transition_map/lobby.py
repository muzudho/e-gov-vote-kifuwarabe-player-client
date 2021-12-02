from app import app
from state_machine_py.abstract_state import AbstractState
from context import Context


class LobbyState(AbstractState):

    def __init__(self):
        super().__init__()

    @property
    def name(self):
        return "[Lobby]"

    def on_begin_game_summary(context):
        pass

    def leave(self, context, line):
        """次の辺の名前を返します
        Parameters
        ----------
        str : line
            文字列（末尾に改行なし）

        Returns
        -------
        str
            辺の名前
        """

        # ----[BEGIN Game_Summary]---->
        #      ------------------
        #      1. 対局条件通知開始
        if line == 'BEGIN Game_Summary':
            self.on_begin_game_summary(context)
            return '----BeginGameSummary---->'

        app.log.write_by_internal(
            f"[DEBUG] Unknown line=[{line}]")
        return '----Loopback---->'


# Test
# python.exe -m floodgate_client.layer1_transition_map.lobby
if __name__ == "__main__":
    app.log.set_up()
    context = Context()
    state = LobbyState()

    line = 'xxxxxxx'
    edge_name = state.leave(context, line)
    if edge_name == '----Loopback---->':
        app.log.write_by_internal('.', end='')
    else:
        app.log.write_by_internal('f', end='')
