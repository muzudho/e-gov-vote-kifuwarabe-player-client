from state_machine_py.abstract_state import AbstractState
from floodgate.keywords import GAME


class GameState(AbstractState):
    def __init__(self):
        super().__init__()

    @property
    def name(self):
        return GAME

    def entry(self, req):
        super().entry(req)

        edge_path = ".".join(req.edge_path)

        return None
