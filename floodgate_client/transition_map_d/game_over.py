import re
from app import app
from state_machine_d.abstract_state import AbstractState
from context import Context


class GameOverState(AbstractState):
    """自分に無限にループバックしているだけの状態です"""

    def __init__(self):
        super().__init__()

    @property
    def name(self):
        return "[GameOver]"

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
        pass

        app.log.write_by_internal(
            f"[DEBUG] Unknown line=[{line}]")
        return '----Loopback---->'


# Test
# python.exe -m floodgate_client.state_d.game_over
if __name__ == "__main__":
    app.log.set_up()
    context = Context()
    state = GameOverState()

    line = 'xxxxxxxxxxxxxx'
    edge_name = state.leave(context, line)
    if edge_name == '----Loopback---->':
        print('.', end='')
    else:
        print('f', end='')
