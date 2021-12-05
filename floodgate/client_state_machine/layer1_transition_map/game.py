from state_machine_py.abstract_state import AbstractState
from floodgate.keywords import E_COMPLETED, E_FLOODGATE, E_GAME_OVER, E_GAME_SUMMARY, E_LOGOUT, E_MOVE_C, E_MOVE_S, E_WCSC, GAME


class GameState(AbstractState):
    def __init__(self):
        super().__init__()

    @property
    def name(self):
        return GAME

    def entry(self, req):
        super().entry(req)

        edge_path = ".".join(req.edge_path)

        if edge_path == "":
            pass
        elif edge_path == f"{E_MOVE_C}":
            pass
        elif edge_path == f"{E_MOVE_S}":
            pass
        elif edge_path == f"{E_GAME_OVER}":
            pass
        elif edge_path == f"{E_GAME_OVER}.{E_FLOODGATE}":
            pass
        elif edge_path == f"{E_GAME_OVER}.{E_WCSC}":
            pass
        else:
            raise ValueError(f"Edge path {edge_path} is not found")

        return None

    def on_move_c(self, req):
        pass

    def on_move_s(self, req):
        pass

    def on_game_over(self, req):
        pass

    def on_floodgate(self, req):
        pass

    def on_wcsc(self, req):
        pass
