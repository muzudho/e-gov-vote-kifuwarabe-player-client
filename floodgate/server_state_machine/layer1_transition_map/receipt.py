import re
from app import app
from state_machine_py.abstract_state import AbstractState
from floodgate.keywords import RECEIPT


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
        return RECEIPT

    def entry(self, req):
        super().entry(req)

        edge_path = ".".join(req.edge_path)

        return None

    def exit(self, req):
        """次の辺の名前を返します

        Parameters
        ----------
        req : Request
            ステートマシンからステートへ与えられる引数のまとまり

        Returns
        -------
        str
            辺の名前
        """

        # ----Ok---->
        matched = self._ok_pattern.match(req.line)
        if matched:
            req.context.user_name = matched.group(1)

            self.on_ok(req)

            return '----Ok---->'

        app.log.write_by_internal(f'処理できなかったline=[{req.line}]')

        return '----InvalidOperation---->'

    def on_ok(self, req):
        pass
