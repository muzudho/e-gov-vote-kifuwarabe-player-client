import re
from app import app
from state_machine_py.abstract_state import AbstractState
from context import Context


class InitState(AbstractState):
    def __init__(self):
        super().__init__()

    @property
    def name(self):
        return "[Init]"

    def entry(self, context):
        super().entry(context)
        return "pass_on"

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
        app.log.write_by_internal('leaveします (init.py 36)')

        if line == 'pass_on':
            self.on_login(context)
            return '----Login---->'

        app.log.write_by_internal(f'処理できなかったline=[{line}]')

        return '----InvalidOperation---->'

    def on_login(self, context):
        app.log.write_by_internal('on_loginしました (init.py 21)')
        pass


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
