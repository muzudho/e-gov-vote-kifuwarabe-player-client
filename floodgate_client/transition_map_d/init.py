import re
from app import app
from state_machine_d.abstract_state import AbstractState
from context import Context


class InitState(AbstractState):
    def __init__(self):
        super().__init__()

        self._ok_pattern = None

    @property
    def name(self):
        return "[Init]"

    @property
    def ok_pattern(self):
        """ログイン
        [LOGIN:e-gov-vote-kifuwarabe OK]
               ---------------------
               1. username
        """
        if self._ok_pattern is None:
            self._ok_pattern = re.compile(r'^LOGIN:([0-9A-Za-z_-]{1,32}) OK$')

        return self._ok_pattern

    def on_ok(self, context):
        """----Ok---->時"""
        pass

    def leave(self, context, line):
        """次の辺の名前を返します
        Parameters
        ----------
        str : line
            入力文字列

        Returns
        -------
        str
            辺の名前
        """

        # ----Ok---->
        matched = self.ok_pattern.match(line)
        if matched:
            context.user_name = matched.group(1)

            self.on_ok(context)

            return '----Ok---->'

        return '----Fail---->'


# Test
# python.exe -m floodgate_client.state_d.init
if __name__ == "__main__":
    app.log.set_up()
    context = Context()
    state = InitState()

    line = 'LOGIN:egov-kifuwarabe OK'
    edge_name = state.leave(context, line)
    if edge_name == '----Ok---->':
        app.log.write_by_internal('.', end='')
    else:
        app.log.write_by_internal('f', end='')
