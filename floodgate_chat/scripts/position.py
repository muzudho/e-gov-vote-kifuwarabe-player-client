import re


class Position():
    def __init__(self):

        # 将棋盤
        self._board = [''] * 100

        # 持駒の数 [未使用, ▲飛, ▲角, ▲金, ▲銀, ▲桂, ▲香, ▲歩, ▽飛, ▽角, ▽金, ▽銀, ▽桂, ▽香, ▽歩]
        self._hands = [0] * 15

        # 手番
        self._turn = '+'

        # 経過時間 [未使用, 先手, 後手]
        self._expend_times = [0, 0, 0]

    @property
    def board(self):
        return self._board

    @property
    def hands(self):
        return self._hands

    def formatBoard(self):
        """将棋盤の文字列"""

        text = ''

        def __prettyHands(indexes):
            def __eraseZero(n):
                if n == 0:
                    return ''
                return n

            a = '{: >3}'.format(__eraseZero(self._hands[indexes[0]]))
            b = '{: >3}'.format(__eraseZero(self._hands[indexes[1]]))
            c = '{: >3}'.format(__eraseZero(self._hands[indexes[2]]))
            d = '{: >3}'.format(__eraseZero(self._hands[indexes[3]]))
            e = '{: >3}'.format(__eraseZero(self._hands[indexes[4]]))
            f = '{: >3}'.format(__eraseZero(self._hands[indexes[5]]))
            g = '{: >3}'.format(__eraseZero(self._hands[indexes[6]]))
            return a, b, c, d, e, f, g

        def __prettyBoardRow(indexes):
            def __eraseAsterisk(s):
                if s == ' * ':
                    return '   '
                return s

            a = '{: >3}'.format(__eraseAsterisk(self._board[indexes[0]]))
            b = '{: >3}'.format(__eraseAsterisk(self._board[indexes[1]]))
            c = '{: >3}'.format(__eraseAsterisk(self._board[indexes[2]]))
            d = '{: >3}'.format(__eraseAsterisk(self._board[indexes[3]]))
            e = '{: >3}'.format(__eraseAsterisk(self._board[indexes[4]]))
            f = '{: >3}'.format(__eraseAsterisk(self._board[indexes[5]]))
            g = '{: >3}'.format(__eraseAsterisk(self._board[indexes[6]]))
            h = '{: >3}'.format(__eraseAsterisk(self._board[indexes[7]]))
            i = '{: >3}'.format(__eraseAsterisk(self._board[indexes[8]]))
            return a, b, c, d, e, f, g, h, i

        tu = f"{self._turn: >4}"
        text += f"""
Turn
{tu}

"""

        # 後手の持ち駒、経過時間
        tim2 = f'{self._expend_times[2]: >6}'
        a, b, c, d, e, f, g = __prettyHands([8, 9, 10, 11, 12, 13, 14])
        text += f"""   TIME   HI  KA  KI  GI  KE  KY  FU
 {tim2} |{a} {b} {c} {d} {e} {f} {g}|
 
 """

        # 盤
        text += f"""  9   8   7   6   5   4   3   2   1    
+---+---+---+---+---+---+---+---+---+  
"""
        a, b, c, d, e, f, g, h, i = __prettyBoardRow(
            [91, 81, 71, 61, 51, 41, 31, 21, 11])
        text += f"""|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 1
+---+---+---+---+---+---+---+---+---+  
"""
        a, b, c, d, e, f, g, h, i = __prettyBoardRow(
            [92, 82, 72, 62, 52, 42, 32, 22, 12])
        text += f"""|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 2
+---+---+---+---+---+---+---+---+---+  
"""
        a, b, c, d, e, f, g, h, i = __prettyBoardRow(
            [93, 83, 73, 63, 53, 43, 33, 23, 13])
        text += f"""|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 3
+---+---+---+---+---+---+---+---+---+  
"""
        a, b, c, d, e, f, g, h, i = __prettyBoardRow(
            [94, 84, 74, 64, 54, 44, 34, 24, 14])
        text += f"""|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 4
+---+---+---+---+---+---+---+---+---+  
"""
        a, b, c, d, e, f, g, h, i = __prettyBoardRow(
            [95, 85, 75, 65, 55, 45, 35, 25, 15])
        text += f"""|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 5
+---+---+---+---+---+---+---+---+---+  
"""
        a, b, c, d, e, f, g, h, i = __prettyBoardRow(
            [96, 86, 76, 66, 56, 46, 36, 26, 16])
        text += f"""|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 6
+---+---+---+---+---+---+---+---+---+  
"""
        a, b, c, d, e, f, g, h, i = __prettyBoardRow(
            [97, 87, 77, 67, 57, 47, 37, 27, 17])
        text += f"""|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 7
+---+---+---+---+---+---+---+---+---+  
"""
        a, b, c, d, e, f, g, h, i = __prettyBoardRow(
            [98, 88, 78, 68, 58, 48, 38, 28, 18])
        text += f"""|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 8
+---+---+---+---+---+---+---+---+---+  
"""
        a, b, c, d, e, f, g, h, i = __prettyBoardRow(
            [99, 89, 79, 69, 59, 49, 39, 29, 19])
        text += f"""|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 9
+---+---+---+---+---+---+---+---+---+  
"""
        # 先手の経過時間、持ち駒
        tim1 = f'{self._expend_times[1]: >6}'
        a, b, c, d, e, f, g = __prettyHands([1, 2, 3, 4, 5, 6, 7])
        text += f"""
   Time   HI  KA  KI  GI  KE  KY  FU  
 {tim1} |{a} {b} {c} {d} {e} {f} {g}|

. . . . . . . . . . . . . . . . . . . .

"""
        return text


# Test
# python.exe "./scripts/position.py"
if __name__ == "__main__":

    position = Position()
    text = position.formatBoard()
    print(text)

    # 開始局面
    # Example:
    # P1-KY-KE-GI-KI-OU-KI-GI-KE-KY
    # P2 * -HI *  *  *  *  * -KA *
    # P3-FU-FU-FU-FU-FU-FU-FU-FU-FU
    # P4 *  *  *  *  *  *  *  *  *
    # P5 *  *  *  *  *  *  *  *  *
    # P6 *  *  *  *  *  *  *  *  *
    # P7+FU+FU+FU+FU+FU+FU+FU+FU+FU
    # P8 * +KA *  *  *  *  * +HI *
    # P9+KY+KE+GI+KI+OU+KI+GI+KE+KY

    position.parse_line('P1-KY-KE-GI-KI-OU-KI-GI-KE-KY')
    text = position.formatBoard()
    print(text)

    position.parse_line('P2 * -HI *  *  *  *  * -KA * ')
    text = position.formatBoard()
    print(text)

    position.parse_line('P3-FU-FU-FU-FU-FU-FU-FU-FU-FU')
    text = position.formatBoard()
    print(text)

    position.parse_line('P4 *  *  *  *  *  *  *  *  * ')
    text = position.formatBoard()
    print(text)

    position.parse_line('P5 *  *  *  *  *  *  *  *  * ')
    text = position.formatBoard()
    print(text)

    position.parse_line('P6 *  *  *  *  *  *  *  *  * ')
    text = position.formatBoard()
    print(text)

    position.parse_line('P7+FU+FU+FU+FU+FU+FU+FU+FU+FU')
    text = position.formatBoard()
    print(text)

    position.parse_line('P8 * +KA *  *  *  *  * +HI * ')
    text = position.formatBoard()
    print(text)

    position.parse_line('P9+KY+KE+GI+KI+OU+KI+GI+KE+KY')
    text = position.formatBoard()
    print(text)

    # 指し手
    # Example: +7776FU,T20
    # Example: -8384FU,T1

    position.parse_line('+7776FU,T20')
    text = position.formatBoard()
    print(text)

    position.parse_line('-8384FU,T1')
    text = position.formatBoard()
    print(text)
