import re
from floodgate_chat.client_state_diagram_d.context import Context
from floodgate_chat.scripts.position import Position


class LoggedInChoice():

    def __init__(self):
        # [Game_ID:wdoor+floodgate-300-10F+Yss1000k+e-gov-vote-kifuwarabe+20211103193002]
        #          ---------------------------------------------------------------------
        #          1. game_id
        self._game_id_pattern = re.compile(r'^Game_ID:([0-9A-Za-z_+-]+)$')
        self._game_id = ''

        # [Name+:John]
        # [Name-:John]
        #      - ----
        #      | |
        #      +------- 1. (+)先手、(-)後手
        #        +----- 2. プレイヤー名
        self._player_name_pattern = re.compile(
            r'^Name([+-]):([0-9A-Za-z_-]+)$')
        # プレイヤー名 [未使用, 先手プレイヤー名, 後手プレイヤー名]
        self._player_names = ['', '', '']

        # [Your_Turn:+]
        #            -
        #            1. わたしの手番(+)(-)
        self._my_turn_pattern = re.compile(
            r'^Your_Turn:([+-])$')
        self._my_turn = ''

        # [To_Move:+]
        #          -
        #          1. 開始局面での手番(+)(-)
        self._startpos_turn_pattern = re.compile(
            r'^To_Move:([+-])$')
        self._startpos_turn = ''

        # [START:wdoor+floodgate-300-10F+e-gov-vote-kifuwarabe+Kristallweizen-Core2Duo-P7450+20211105220005]
        #        ------------------------------------------------------------------------------------------
        #        1. game_id
        self._start_pattern = re.compile(r'^START:([0-9A-Za-z_+-]+)$')
        self._start_game_id = ''

        # [P1-KY-KE-GI-KI-OU-KI-GI-KE-KY
        #  P2 * -HI *  *  *  *  * -KA *
        #  P3-FU-FU-FU-FU-FU-FU-FU-FU-FU
        #  P4 *  *  *  *  *  *  *  *  *
        #  P5 *  *  *  *  *  *  *  *  *
        #  P6 *  *  *  *  *  *  *  *  *
        #  P7+FU+FU+FU+FU+FU+FU+FU+FU+FU
        #  P8 * +KA *  *  *  *  * +HI *
        #  P9+KY+KE+GI+KI+OU+KI+GI+KE+KY]
        #  -----------------------------
        #  開始局面の各行
        self._begin_pos_row_pattern = re.compile(
            r"^P(\d)(.{3})(.{3})(.{3})(.{3})(.{3})(.{3})(.{3})(.{3})(.{3})$")

        self._position = Position()

        def none_func():
            pass

        # --GameId-- 時のコールバック関数
        self._on_game_id = none_func

        # --EndGameSummary-- 時のコールバック関数
        self._on_end_game_summary = none_func

        # --Start-- 時のコールバック関数
        self._on_start = none_func

    @property
    def name(self):
        return "[LoggedIn]<LoggedIn>"

    @property
    def game_id(self):
        return self._game_id

    @property
    def start_game_id(self):
        return self._start_game_id

    @property
    def my_turn(self):
        return self._my_turn

    @property
    def position(self):
        return self._position

    @property
    def player_names(self):
        return self._player_names

    @property
    def my_turn(self):
        return self._my_turn

    @property
    def startpos_turn(self):
        return self._startpos_turn

    @property
    def on_game_id(self):
        """--GameId--時のコールバック関数"""
        return self._on_game_id

    @on_game_id.setter
    def on_game_id(self, func):
        self._on_game_id = func

    @property
    def on_end_game_summary(self):
        """--EndGameSummary--時のコールバック関数"""
        return self._on_end_game_summary

    @on_end_game_summary.setter
    def on_end_game_summary(self, func):
        self._on_end_game_summary = func

    @property
    def on_start(self):
        """--Start--時のコールバック関数"""
        return self._on_start

    @on_start.setter
    def on_start(self, func):
        self._on_start = func

    def forward(self, context, line):
        """状態遷移します
        Parameters
        ----------
        str : line
            辺の名前
        """

        # ----[END Game_Summary]---->
        #      ----------------
        #      初期局面終了
        if line == 'END Game_Summary':
            self.on_end_game_summary()
            return '--EndGameSummary--'

        # ----[Name+:John]---->
        #     [Name-:John]
        #          - ----
        #          | |
        #          +------- 1. (+)先手、(-)後手
        #            +----- 2. プレイヤー名
        matched = self._player_name_pattern.match(line)
        if matched:
            turn = matched.group(1)
            if turn == '+':
                self._player_names[1] = matched.group(2)
            elif turn == '-':
                self._player_names[2] = matched.group(2)
            else:
                # Error
                raise ValueError(f'ここにはこないはず')

            return '--Turn--'

        # ----[Your_Turn:+]---->
        #                -
        #                1. わたしの手番(+)(-)
        matched = self._my_turn_pattern.match(line)
        if matched:
            self._my_turn = matched.group(1)
            return '--MyTurn--'

        # ----[To_Move:+]---->
        #              -
        #              1. 開始局面での手番(+)(-)
        matched = self._startpos_turn_pattern.match(line)
        if matched:
            self._startpos_turn = matched.group(1)
            return '--StartPosTurn--'

        # ----[Game_ID:wdoor+floodgate-300-10F+Yss1000k+e-gov-vote-kifuwarabe+20211103193002]----> ログイン成功
        #              ---------------------------------------------------------------------
        #              1. game_id
        matched = self._game_id_pattern.match(line)
        if matched:
            self._game_id = matched.group(1)

            self.on_game_id()

            return '--GameId--'

        # ----[開始局面の各行]---->
        matched = self._begin_pos_row_pattern.match(line)
        if matched:
            rank = int(matched.group(1))
            self._position.board[90 + rank] = matched.group(2)
            self._position.board[80 + rank] = matched.group(3)
            self._position.board[70 + rank] = matched.group(4)
            self._position.board[60 + rank] = matched.group(5)
            self._position.board[50 + rank] = matched.group(6)
            self._position.board[40 + rank] = matched.group(7)
            self._position.board[30 + rank] = matched.group(8)
            self._position.board[20 + rank] = matched.group(9)
            self._position.board[10 + rank] = matched.group(10)

            return '--BeginPosRow--'

        # ----[START:wdoor+floodgate-300-10F+e-gov-vote-kifuwarabe+Kristallweizen-Core2Duo-P7450+20211105220005]----> 対局合意成立
        #            ------------------------------------------------------------------------------------------
        #            1. game_id
        matched = self._start_pattern.match(line)
        if matched:
            self._start_game_id = matched.group(1)

            self.on_start()

            return '--Start--'

        return '--Unknown--'


# Test
# python.exe -m floodgate_chat.client_state_diagram_d.logged_in_state
if __name__ == "__main__":
    context = Context()
    state = LoggedInChoice()

    line = 'Game_ID:wdoor+floodgate-300-10F+Yss1000k+e-gov-vote-kifuwarabe+20211103193002'
    edge = state.forward(context, line)
    if edge == '--GameId--':
        print('.', end='')
    else:
        print('f', end='')

    line = 'P1-KY-KE-GI-KI-OU-KI-GI-KE-KY'
    edge = state.forward(context, line)
    if edge == '--BeginPosRow--':
        print('.', end='')
    else:
        print('f', end='')

    line = 'START:wdoor+floodgate-300-10F+e-gov-vote-kifuwarabe+Kristallweizen-Core2Duo-P7450+20211105220005'
    edge = state.forward(context, line)
    if edge == '--Start--':
        print('.', end='')
    else:
        print('f', end='')
