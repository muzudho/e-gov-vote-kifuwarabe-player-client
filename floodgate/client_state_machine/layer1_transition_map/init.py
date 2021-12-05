import re
from app import app
from state_machine_py.abstract_state import AbstractState
from context import Context
from floodgate.keywords import E_INCORRECT, E_LOGIN, E_OK, INIT


class InitState(AbstractState):
    def __init__(self):
        super().__init__()

    @property
    def name(self):
        return INIT

    def entry(self, req):
        super().entry(req)

        edge_path = ".".join(req.edge_path)

        if edge_path == "":
            return "pass_on"
        elif edge_path == f"{E_LOGIN}":
            pass
        elif edge_path == f"{E_LOGIN}.{E_OK}":
            pass
        elif edge_path == f"{E_LOGIN}.{E_INCORRECT}":
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
        edge_path = ".".join(req.edge_path)

        if req.line == 'pass_on':
            if edge_path == "":
                self.on_login(context)
                return E_LOGIN

        app.log.write_by_internal(f'処理できなかったline=[{line}]')

        return '----InvalidOperation---->'

    def on_login(self, req):
        pass

    def on_ok(self, req):
        pass

    def on_incorrect(self, req):
        pass


# Test
# python.exe -m floodgate_client_state.state_d.init
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
