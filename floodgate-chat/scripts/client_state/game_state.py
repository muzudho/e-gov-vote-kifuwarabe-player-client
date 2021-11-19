import re
from scripts.position import Position


class GameState():
    """`START:` してからの状態"""

    def __init__(self):

        # 自分または相手の指し手と、その消費時間
        # Format: `<先後><元升><先升><駒>,T<秒>`
        # Example: `+5756FU,T20`
        self._move_pattern = re.compile(
            r"^([+-])(\d{2})(\d{2})(\w{2}),T(\d+)$")

        # プレイヤー名 [未使用, 先手プレイヤー名, 後手プレイヤー名]
        self._player_names = ['', '', '']

        # 局面
        self._position = Position()

    @property
    def name(self):
        return "<GameState/>"

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, val):
        self._position = val

    @property
    def player_names(self):
        return self._player_names

    @player_names.setter
    def player_names(self, val):
        self._player_names = val

    def parse_line(self, line):

        # 指し手
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

            return '<Position.Move/>'

        if line == '#WIN':
            # 勝ち
            return '<Position.Win/>'

        if line == '#LOSE':
            # 負け
            return '<Position.Lose/>'

        return '<Position.Unknown/>'


# Test
# python.exe "./scripts/client_state/game_state.py"
if __name__ == "__main__":
    line = 'LOGIN:egov-kifuwarabe OK'

    none_state = GameState()
    result = none_state.parse_line(line)
    if result == '<NoneState.LoginOk/>':
        print('.', end='')
    else:
        print('f', end='')
