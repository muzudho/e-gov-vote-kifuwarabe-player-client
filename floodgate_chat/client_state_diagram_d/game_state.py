import re
from floodgate_chat.client_state_diagram_d.context import Context
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

        def none_func(context):
            return '--Unimplemented--'

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
            expendTime = int(result.group(5))

            piece = result.group(4)
            srcPc = context.position.board[source]  # sourcePiece
            dstPc = context.position.board[destination]  # destinationPiece
            # print(f"Move> {result.group(0)} [phase]{phase:>2} [source]{source:>2} [destination]{destination} [piece]{piece} srcPc[{srcPc}] dstPc[{dstPc}]")
            if source != 0 and srcPc == ' * ':
                raise Exception("空マスから駒を動かそうとしました")

            # 駒を打つとき、駒台から減らす
            if source == 0:
                if phase == '+':
                    srcPc = '+{}'.format(piece)
                    if piece == 'FU':
                        context.position.hands[7] -= 1
                    elif piece == 'KY':
                        context.position.hands[6] -= 1
                    elif piece == 'KE':
                        context.position.hands[5] -= 1
                    elif piece == 'GI':
                        context.position.hands[4] -= 1
                    elif piece == 'KI':
                        context.position.hands[3] -= 1
                    elif piece == 'KA':
                        context.position.hands[2] -= 1
                    elif piece == 'HI':
                        context.position.hands[1] -= 1
                    else:
                        raise Exception(f"+ phase={phase} piece={piece}")
                elif phase == '-':
                    srcPc = '-{}'.format(piece)
                    if piece == 'FU':
                        context.position.hands[14] -= 1
                    elif piece == 'KY':
                        context.position.hands[13] -= 1
                    elif piece == 'KE':
                        context.position.hands[12] -= 1
                    elif piece == 'GI':
                        context.position.hands[11] -= 1
                    elif piece == 'KI':
                        context.position.hands[10] -= 1
                    elif piece == 'KA':
                        context.position.hands[9] -= 1
                    elif piece == 'HI':
                        context.position.hands[8] -= 1
                    else:
                        raise Exception(f"- phase={phase} piece={piece}")

            # 移動先に駒があれば駒台へ移動
            if phase == '+':
                if dstPc == "-FU" or dstPc == "-TO":
                    context.position.hands[7] += 1
                elif dstPc == "-KY" or dstPc == "-NY":
                    context.position.hands[6] += 1
                elif dstPc == "-KE" or dstPc == "-NK":
                    context.position.hands[5] += 1
                elif dstPc == "-GI" or dstPc == "-NG":
                    context.position.hands[4] += 1
                elif dstPc == "-KI":
                    context.position.hands[3] += 1
                elif dstPc == "-KA" or dstPc == "-UM":
                    context.position.hands[2] += 1
                elif dstPc == "-HI" or dstPc == "-RY":
                    context.position.hands[1] += 1
                elif dstPc == "-OU":
                    pass
            elif phase == '-':
                if dstPc == "+FU" or dstPc == "+TO":
                    context.position.hands[14] += 1
                elif dstPc == "+KY" or dstPc == "+NY":
                    context.position.hands[13] += 1
                elif dstPc == "+KE" or dstPc == "+NK":
                    context.position.hands[12] += 1
                elif dstPc == "+GI" or dstPc == "+NG":
                    context.position.hands[11] += 1
                elif dstPc == "+KI":
                    context.position.hands[10] += 1
                elif dstPc == "+KA" or dstPc == "+UM":
                    context.position.hands[9] += 1
                elif dstPc == "+HI" or dstPc == "+RY":
                    context.position.hands[8] += 1
                elif dstPc == "+OU":
                    pass
            else:
                raise Exception(f"Caputure piece. phase={phase}")

            # 移動元の駒を消す
            context.position.board[source] = " * "

            # 移動先に駒を置く
            context.position.board[destination] = srcPc

            # 経過時間
            if phase == '+':
                context.position._expend_times[1] += expendTime
            else:
                context.position._expend_times[2] += expendTime

            self.on_move(context)
            return '--Move--'

        # ----[#WIN]---->
        #      ----
        #      勝ち
        if line == '#WIN':
            self.on_win(context)
            return '--Win--'

        # ----[#LOSE]---->
        #      -----
        #      負け
        if line == '#LOSE':
            self.on_lose(context)
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
    edge = state.leave(context, line)
    if edge == '--Move--':
        print('.', end='')
    else:
        print('f', end='')
