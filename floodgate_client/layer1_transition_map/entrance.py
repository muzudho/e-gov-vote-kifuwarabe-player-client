import re
from app import app
from state_machine_py.abstract_state import AbstractState
from context import Context


class EntranceState(AbstractState):
    def __init__(self):
        super().__init__()

        """ログインオーケー
        LOGIN:e-gov-vote-kifuwarabe OK
              ---------------------
              1. username
        """
        self._ok_pattern = re.compile(r'^LOGIN:([0-9A-Za-z_-]{1,32}) OK$')

    @property
    def name(self):
        return "[Entrance]"

    def on_entry(self, context):
        pass

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
        matched = self._ok_pattern.match(line)
        if matched:
            context.user_name = matched.group(1)

            self.on_ok(context)

            return '----Ok---->'

        app.log.write_by_internal(f'処理できなかったline=[{line}]')

        return '----InvalidOperation---->'
