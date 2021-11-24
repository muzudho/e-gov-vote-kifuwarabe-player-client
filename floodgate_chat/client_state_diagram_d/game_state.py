import re
from floodgate_chat.client_state_diagram_d.context import Context
from floodgate_chat.scripts.position import Position
from floodgate_chat.scripts.client_socket import client_socket
from floodgate_chat.scripts.log_output import log_output


class GameState():
    """`START:` してからの状態"""

    def __init__(self):

        # [+5756FU,T20]
        #  -            先後(+)(-)
        #   --          元升
        #     --        先升
        #       --      駒
        #          ---  消費時間（秒）
        self._move_pattern = re.compile(
            r"^([+-])(\d{2})(\d{2})(\w{2}),T(\d+)$")

        # 自分の手番符号
        self._my_turn = None

        # プレイヤー名 [未使用, 先手プレイヤー名, 後手プレイヤー名]
        self._player_names = ['', '', '']

        # 局面
        self._position = Position()

        def none_func():
            return "Unimplemented[none_func]"

        # --Move-- 時のコールバック関数
        self._on_move = none_func

        # --Win-- 時のコールバック関数
        self._on_win = none_func

        # --Lose-- 時のコールバック関数
        self._on_lose = none_func

    @property
    def name(self):
        return "[Game]"

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, val):
        self._position = val

    @property
    def my_turn(self):
        return self._my_turn

    @my_turn.setter
    def my_turn(self, val):
        self._my_turn = val

    @property
    def player_names(self):
        return self._player_names

    @player_names.setter
    def player_names(self, val):
        self._player_names = val

    @property
    def on_move(self):
        """--Move--時のコールバック関数"""
        return self._on_move

    @on_move.setter
    def on_move(self, func):
        self._on_move = func

    @property
    def on_win(self):
        """--Win--時のコールバック関数"""
        return self._on_win

    @on_win.setter
    def on_win(self, func):
        self._on_win = func

    @property
    def on_lose(self):
        """--Lose--時のコールバック関数"""
        return self._on_lose

    @on_lose.setter
    def on_lose(self, func):
        self._on_lose = func

    def forward(self, context, line):
        """状態遷移します
        Parameters
        ----------
        str : line
            入力文字列

        Returns
        -------
        str
            次のノード名
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
            expendTime = int(result.group(5))

            piece = result.group(4)
            srcPc = self._position.board[source]  # sourcePiece
            dstPc = self._position.board[destination]  # destinationPiece
            # print(f"Move> {result.group(0)} [phase]{phase:>2} [source]{source:>2} [destination]{destination} [piece]{piece} srcPc[{srcPc}] dstPc[{dstPc}]")
            if source != 0 and srcPc == ' * ':
                raise Exception("空マスから駒を動かそうとしました")

            # 駒を打つとき、駒台から減らす
            if source == 0:
                if phase == '+':
                    srcPc = '+{}'.format(piece)
                    if piece == 'FU':
                        self._position.hands[7] -= 1
                    elif piece == 'KY':
                        self._position.hands[6] -= 1
                    elif piece == 'KE':
                        self._position.hands[5] -= 1
                    elif piece == 'GI':
                        self._position.hands[4] -= 1
                    elif piece == 'KI':
                        self._position.hands[3] -= 1
                    elif piece == 'KA':
                        self._position.hands[2] -= 1
                    elif piece == 'HI':
                        self._position.hands[1] -= 1
                    else:
                        raise Exception(f"+ phase={phase} piece={piece}")
                elif phase == '-':
                    srcPc = '-{}'.format(piece)
                    if piece == 'FU':
                        self._position.hands[14] -= 1
                    elif piece == 'KY':
                        self._position.hands[13] -= 1
                    elif piece == 'KE':
                        self._position.hands[12] -= 1
                    elif piece == 'GI':
                        self._position.hands[11] -= 1
                    elif piece == 'KI':
                        self._position.hands[10] -= 1
                    elif piece == 'KA':
                        self._position.hands[9] -= 1
                    elif piece == 'HI':
                        self._position.hands[8] -= 1
                    else:
                        raise Exception(f"- phase={phase} piece={piece}")

            # 移動先に駒があれば駒台へ移動
            if phase == '+':
                if dstPc == "-FU" or dstPc == "-TO":
                    self._position.hands[7] += 1
                elif dstPc == "-KY" or dstPc == "-NY":
                    self._position.hands[6] += 1
                elif dstPc == "-KE" or dstPc == "-NK":
                    self._position.hands[5] += 1
                elif dstPc == "-GI" or dstPc == "-NG":
                    self._position.hands[4] += 1
                elif dstPc == "-KI":
                    self._position.hands[3] += 1
                elif dstPc == "-KA" or dstPc == "-UM":
                    self._position.hands[2] += 1
                elif dstPc == "-HI" or dstPc == "-RY":
                    self._position.hands[1] += 1
                elif dstPc == "-OU":
                    pass
            elif phase == '-':
                if dstPc == "+FU" or dstPc == "+TO":
                    self._position.hands[14] += 1
                elif dstPc == "+KY" or dstPc == "+NY":
                    self._position.hands[13] += 1
                elif dstPc == "+KE" or dstPc == "+NK":
                    self._position.hands[12] += 1
                elif dstPc == "+GI" or dstPc == "+NG":
                    self._position.hands[11] += 1
                elif dstPc == "+KI":
                    self._position.hands[10] += 1
                elif dstPc == "+KA" or dstPc == "+UM":
                    self._position.hands[9] += 1
                elif dstPc == "+HI" or dstPc == "+RY":
                    self._position.hands[8] += 1
                elif dstPc == "+OU":
                    pass
            else:
                raise Exception(f"Caputure piece. phase={phase}")

            # 移動元の駒を消す
            self._position.board[source] = " * "

            # 移動先に駒を置く
            self._position.board[destination] = srcPc

            # 経過時間
            if phase == '+':
                self._position._expend_times[1] += expendTime
            else:
                self._position._expend_times[2] += expendTime

            self.on_move()
            return '--Move--'

        # ----[#WIN]---->
        #      ----
        #      勝ち
        if line == '#WIN':
            self.on_win()
            return '--Win--'

        # ----[#LOSE]---->
        #      -----
        #      負け
        if line == '#LOSE':
            self.on_lose()
            return '--Lose--'

        # ----[??????]---->
        #      ------
        #      その他
        return '--Unknown--'


# Test
# python.exe -m floodgate_chat.client_state_diagram_d.game_state
if __name__ == "__main__":
    context = Context()
    state = GameState()

    line = '+5756FU,T20'
    edge = state.forward(context, line)
    if edge == '--Move--':
        print('.', end='')
    else:
        print('f', end='')
