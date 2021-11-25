from floodgate_chat.scripts.log_output import log_output


class StateMachine():
    """状態遷移マシーン（State diagram machine）"""

    def __init__(self, context=None, state_creators={}, transition_dict={}):
        """初期化

        Parameters
        ----------
        context : Context
            Defaults to None.
        state_creators : dict
            状態を作成する関数のディクショナリーです。 Defaults to {}.
        transition_dict : dict
            Defaults to {}.
        """
        self._context = context
        self._state_creators = state_creators
        self._transition_dict = transition_dict
        # 初期状態
        self._state = self._state_creators[""]()

    @property
    def context(self):
        """グローバル変数みたいなもん。StateMachineは内容を知りません"""
        return self._context

    @context.setter
    def context(self, val):
        self._context = val

    @property
    def state(self):
        return self._state

    def leave(self, line):
        """次の状態の名前と、遷移に使ったキーを返します
        Parameters
        ----------
        str : line
            入力文字列（末尾に改行なし）

        Returns
        -------
        str, str
            次の状態の名前、遷移に使ったキー
        """

        edge_name = self._state.leave(self._context, line)

        # さっき去ったステートの名前と、今辿っているエッジの名前
        key = f"{self._state.name}{edge_name}"

        if key in self._transition_dict:
            return self._transition_dict[key], key

        self._state.on_exit(self._context)

        return None, key

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

        if next_state_name in self._state_creators:
            # 次のステートへ引継ぎ
            self._state = self._state_creators[next_state_name]()

            self._state.on_entry(self._context)

        else:
            # Error
            raise ValueError(f"Next state [{next_state_name}] is None")
