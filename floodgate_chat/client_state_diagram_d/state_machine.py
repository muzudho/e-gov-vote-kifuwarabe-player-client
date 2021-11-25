import time
from floodgate_chat.client_state_diagram_d.context import Context
from floodgate_chat.client_state_diagram_d.mapping import connection_dict
from floodgate_chat.scripts.log_output import log_output


class StateMachine():
    def __init__(self):
        # グローバル変数みたいなもん
        self._context = Context()

        self._state_creators = {}

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, val):
        self._context = val

    @property
    def state(self):

        if self._state is None:
            # 初期状態
            self._state = self._state_creators[""]()

        return self._state

    @property
    def state_creators(self):
        """状態を作成する関数のディクショナリーです"""
        return self._state_creators

    def leave(self, line):
        """次の辺の名前を返します
        Parameters
        ----------
        str : line
            入力文字列（末尾に改行なし）

        Returns
        -------
        str
            次の状態の名前
        """

        edge_name = self._state.leave(self._context, line)

        # さっき去ったステートの名前と、今辿っているエッジの名前
        key = f"{self._state.name}{edge_name}"

        if key in connection_dict:
            return connection_dict[key]

        log_output.display_and_log_internal(
            f"[DEBUG] state=[{self._state.name}] edge=[{edge_name}]")

        return None

    def arrive(self, next_state_name):
        """次の節の名前を返します
        Parameters
        ----------
        str : next_state_name
            次の状態の名前

        Returns
        -------
        str
            節の名前
        """

        if next_state_name == "[GameSummary]":
            # 次のステートへ引継ぎ
            self._state = self._state_creators["[GameSummary]"]()
        else:
            # Error
            raise ValueError(f"Next sate [{next_state_name}] is None")
