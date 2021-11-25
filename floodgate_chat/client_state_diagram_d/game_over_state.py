import re
from state_machine_d.abstract_state import AbstractState
from floodgate_chat.scripts.log_output import log_output
from floodgate_chat.client_state_diagram_d.context import Context


class GameOverState(AbstractState):

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

        log_output.display_and_log_internal(
            f"[DEBUG] Unknown line=[{line}]")
        return '----Loopback---->'


# Test
# python.exe -m floodgate_chat.client_state_diagram_d.game_over_state
if __name__ == "__main__":
    log_output.set_up()
    context = Context()
    state = GameOverState()

    line = 'xxxxxxxxxxxxxx'
    edge_name = state.leave(context, line)
    if edge_name == '----Loopback---->':
        print('.', end='')
    else:
        print('f', end='')
