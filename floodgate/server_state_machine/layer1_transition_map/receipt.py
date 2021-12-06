import re
import time
from app import app
from state_machine_py.abstract_state import AbstractState
from floodgate.keywords import E_EMPTY, E_INCORRECT, E_LOGIN, E_OK, RECEIPT


class ReceiptState(AbstractState):
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

        edge_path = "/".join(req.edge_path)

        if edge_path == "":
            return "pass_on"
        elif edge_path == f"{E_LOGIN}":
            pass
        elif edge_path == f"{E_LOGIN}/{E_OK}":
            pass
        elif edge_path == f"{E_LOGIN}/{E_INCORRECT}":
            pass
        else:
            raise ValueError(f"Edge path {edge_path} is not found")

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

        edge_path = "/".join(req.edge_path)

        if edge_path == "":
            # Clientのターン
            time.sleep(0.1)
            return E_EMPTY

        elif edge_path == f"{E_LOGIN}":
            # ----Ok---->
            matched = self._ok_pattern.match(req.line)
            if matched:
                req.context.user_name = matched.group(1)

                self.on_ok(req)
                return E_OK

        else:
            raise ValueError(f"Edge path {edge_path} is not found")

        msg = f'処理できなかったline=[{req.line}] edge_path={edge_path}'
        app.log.write_by_internal(msg)
        raise ValueError(msg)

    def on_ok(self, req):
        pass

    def on_incorrect(self, req):
        pass
