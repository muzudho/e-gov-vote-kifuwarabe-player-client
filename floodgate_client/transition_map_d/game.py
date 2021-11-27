import re
from app import app
from shogi_d.csa_helper import do_move
from state_machine_d.abstract_state import AbstractState
from floodgate_client.context import Context


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
            pass

        # ----Move----> 時のコールバック関数
        self._on_move = none_func

        # ----Win----> 時のコールバック関数
        self._on_win = none_func

        # ----Lose----> 時のコールバック関数
        self._on_lose = none_func

        # ----IllegalMove----> 時のコールバック関数
        self._on_illegal_move = none_func

        # ----TimeUp----> 時のコールバック関数
        self._on_time_up = none_func

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

    @property
    def on_illegal_move(self):
        """----IllegalMove---->時のコールバック関数"""
        return self._on_illegal_move

    @on_illegal_move.setter
    def on_illegal_move(self, func):
        self._on_illegal_move = func

    @property
    def on_time_up(self):
        """----TimeUp---->時のコールバック関数"""
        return self._on_time_up

    @on_time_up.setter
    def on_time_up(self, func):
        self._on_time_up = func

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

        # ----[#ILLEGAL_MOVE]---->
        #      -------------
        #      非合法手
        if line == '#ILLEGAL_MOVE':
            self.on_illegal_move(context)
            return '----Loopback---->'

        # ----[#TIME_UP]---->
        #      -------------
        #      時間切れ
        if line == '#TIME_UP':
            self.on_time_up(context)
            return '----Loopback---->'

        # ----[??????]---->
        #      ------
        #      その他
        return '----Unknown1---->'


# Test
# python.exe -m floodgate_client.state_d.game
if __name__ == "__main__":
    app.log.set_up()
    context = Context()
    state = GameState()

    line = '+5756FU,T20'
    edge_name = state.leave(context, line)
    if edge_name == '----Move---->':
        print('.', end='')
    else:
        print('f', end='')
