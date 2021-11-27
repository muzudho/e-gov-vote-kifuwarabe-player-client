import re
from app import app
from state_machine_d.abstract_state import AbstractState
from context import Context


class InitState(AbstractState):
    def __init__(self):
        super().__init__()

        self._ok_pattern = None

        def none_func(context):
            return '----Unimplemented---->'

        # ----Ok----> 時のコールバック関数
        self._on_ok = none_func

    @property
    def name(self):
        return "[Init]"

    @property
    def on_ok(self):
        """----Ok---->時のコールバック関数"""
        return self._on_ok

    @on_ok.setter
    def on_ok(self, func):
        self._on_ok = func

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
        print('.', end='')
    else:
        print('f', end='')