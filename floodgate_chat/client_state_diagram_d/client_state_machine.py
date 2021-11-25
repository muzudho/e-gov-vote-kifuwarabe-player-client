from floodgate_chat.client_state_diagram_d.diagram import Diagram


class ClientStateMachine():
    def __init__(self):
        self._diagram = Diagram()

    @property
    def diagram(self):
        """ダイアグラム"""
        return self._diagram
