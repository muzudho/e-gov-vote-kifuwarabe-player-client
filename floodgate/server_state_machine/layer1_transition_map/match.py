from state_machine_py.abstract_state import AbstractState
from floodgate.keywords import E_COMPLETED, E_GAME_SUMMARY, E_LOGOUT, MATCH


class MatchState(AbstractState):
    def __init__(self):
        super().__init__()

    @property
    def name(self):
        return MATCH

    def entry(self, req):
        super().entry(req)

        edge_path = "/".join(req.edge_path)

        if edge_path == "":
            pass
        elif edge_path == f"{E_LOGOUT}":
            pass
        elif edge_path == f"{E_LOGOUT}/{E_COMPLETED}":
            pass
        elif edge_path == f"{E_GAME_SUMMARY}":
            pass
        else:
            raise ValueError(f"Edge path {edge_path} is not found")

        return None

    def on_reject_c(self, req):
        pass

    def on_reject_s(self, req):
        pass

    def on_agree(self, req):
        pass

    def on_start(self, req):
        pass
