import re
from scripts.logger import logger
from shogi_d.csa_helper import do_move
from state_machine_d.abstract_state import AbstractState
from floodgate_chat.client_state_diagram_d.context import Context


class GameState(AbstractState):
    """`START:` してからの状態"""

    def __init__(self):
        super().__init__()

        # [+5756FU,T20]
        #  -            先後(+)(-)
        #   --          元升
        #     --        先升
        #       --      駒
        #          ---  消費時間（秒）
        self._move_pattern = re.compile(
            r"^([+-])(\d{2})(\d{2})(\w{2}),T(\d+)$")

        def none_func(context):
            return '----Unimplemented---->'

        # ----Move----> 時のコールバック関数
        self._on_move = none_func

        # ----Win----> 時のコールバック関数
        self._on_win = none_func

        # ----Lose----> 時のコールバック関数
        self._on_lose = none_func

    @property
    def name(self):
        return "[Game]"

    @property
    def on_move(self):
        """----Move---->時のコールバック関数"""
        return self._on_move

    @on_move.setter
    def on_move(self, func):
        self._on_move = func

    @property
    def on_win(self):
        """----Win---->時のコールバック関数"""
        return self._on_win

    @on_win.setter
    def on_win(self, func):
        self._on_win = func

    @property
    def on_lose(self):
        """----Lose---->時のコールバック関数"""
        return self._on_lose

    @on_lose.setter
    def on_lose(self, func):
        self._on_lose = func

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

        # ----[+5756FU,T20]---->
        #      -            先後(+)(-)
        #       --          元升
        #         --        先升
        #           --      駒
        #              ---  消費時間（秒）
        result = self._move_pattern.match(line)
        if result:
            phase = result.group(1)
            source = int(result.group(2))
            destination = int(result.group(3))
            piece = result.group(4)
            expend_time = int(result.group(5))

            do_move(context.position, phase, source,
                    destination, piece, expend_time)

            self.on_move(context)
            return '----Move---->'

        # ----[#WIN]---->
        #      ----
        #      勝ち
        if line == '#WIN':
            self.on_win(context)
            return '----Win---->'

        # ----[#LOSE]---->
        #      -----
        #      負け
        if line == '#LOSE':
            self.on_lose(context)
            return '----Lose---->'

        # ----[??????]---->
        #      ------
        #      その他
        return '----Unknown1---->'


# Test
# python.exe -m floodgate_chat.client_state_diagram_d.game_state
if __name__ == "__main__":
    logger.set_up()
    context = Context()
    state = GameState()

    line = '+5756FU,T20'
    edge_name = state.leave(context, line)
    if edge_name == '----Move---->':
        print('.', end='')
    else:
        print('f', end='')
