import re
from app import app
from shogi_d.csa_helper import do_move
from state_machine_py.abstract_state import AbstractState
from context import Context


class PlayState(AbstractState):

    def __init__(self):
        super().__init__()

    @property
    def name(self):
        return "[Play]"

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

        # 指し手を送信します
        self.on_my_move(context)

        # 指し手を送信しました
        return '----MyMove---->'

    def on_my_move(context):
        pass
