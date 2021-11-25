import re
from floodgate_chat.client_state_diagram_d.context import Context
from floodgate_chat.scripts.log_output import log_output


class GameSummaryState():

    def __init__(self):
        # [Game_ID:wdoor+floodgate-300-10F+Yss1000k+e-gov-vote-kifuwarabe+20211103193002]
        #          ---------------------------------------------------------------------
        #          1. game_id
        self._game_id_pattern = re.compile(r'^Game_ID:([0-9A-Za-z_+-]+)$')

        # [Name+:John]
        # [Name-:John]
        #      - ----
        #      | |
        #      +------- 1. (+)先手、(-)後手
        #        +----- 2. プレイヤー名
        self._player_name_pattern = re.compile(
            r'^Name([+-]):([0-9A-Za-z_-]+)$')

        # [Your_Turn:+]
        #            -
        #            1. わたしの手番(+)(-)
        self._my_turn_pattern = re.compile(
            r'^Your_Turn:([+-])$')

        # [To_Move:+]
        #          -
        #          1. 開始局面での手番(+)(-)
        self._startpos_turn_pattern = re.compile(
            r'^To_Move:([+-])$')

        # [START:wdoor+floodgate-300-10F+e-gov-vote-kifuwarabe+Kristallweizen-Core2Duo-P7450+20211105220005]
        #        ------------------------------------------------------------------------------------------
        #        1. game_id
        self._start_pattern = re.compile(r'^START:([0-9A-Za-z_+-]+)$')

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

        def none_func(context):
            return '----Unimplemented---->'

        # ----GameId----> 時のコールバック関数
        self._on_game_id = none_func

        # ----EndGameSummary----> 時のコールバック関数
        self._on_end_game_summary = none_func

        # ----Start----> 時のコールバック関数
        self._on_start = none_func

    @property
    def name(self):
        return "[GameSummary]"

    @property
    def on_game_id(self):
        """----GameId---->時のコールバック関数"""
        return self._on_game_id

    @on_game_id.setter
    def on_game_id(self, func):
        self._on_game_id = func

    @property
    def on_end_game_summary(self):
        """----EndGameSummary---->時のコールバック関数"""
        return self._on_end_game_summary

    @on_end_game_summary.setter
    def on_end_game_summary(self, func):
        self._on_end_game_summary = func

    @property
    def on_start(self):
        """[GameSummary].----Start----> 時のコールバック関数"""
        return self._on_start

    @on_start.setter
    def on_start(self, func):
        self._on_start = func

    def leave(self, context, line):
        """次の辺の名前を返します
        Parameters
        ----------
        str : line
            文字列（末尾に改行なし）

        Returns
        -------
        str
            辺の名前
        """

        # ----[END Game_Summary]---->
        #      ----------------
        #      初期局面終了
        if line == 'END Game_Summary':
            self.on_end_game_summary(context)
            return '----Loopback---->'

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
                context.player_names[1] = matched.group(2)
            elif turn == '-':
                context.player_names[2] = matched.group(2)
            else:
                # Error
                raise ValueError(f'ここにはこないはず')

            return '----Loopback---->'

        # ----[Your_Turn:+]---->
        #                -
        #                1. わたしの手番(+)(-)
        matched = self._my_turn_pattern.match(line)
        if matched:
            context.my_turn = matched.group(1)
            return '----Loopback---->'

        # ----[To_Move:+]---->
        #              -
        #              1. 開始局面での手番(+)(-)
        matched = self._startpos_turn_pattern.match(line)
        if matched:
            context.current_turn = matched.group(1)
            return '----Loopback---->'

        # ----[Game_ID:wdoor+floodgate-300-10F+Yss1000k+e-gov-vote-kifuwarabe+20211103193002]----> ログイン成功
        #              ---------------------------------------------------------------------
        #              1. game_id
        matched = self._game_id_pattern.match(line)
        if matched:
            context.game_id = matched.group(1)

            self.on_game_id(context)

            return '----Loopback---->'

        # ----[開始局面の各行]---->
        matched = self._begin_pos_row_pattern.match(line)
        if matched:
            rank = int(matched.group(1))
            context.position.board[90 + rank] = matched.group(2)
            context.position.board[80 + rank] = matched.group(3)
            context.position.board[70 + rank] = matched.group(4)
            context.position.board[60 + rank] = matched.group(5)
            context.position.board[50 + rank] = matched.group(6)
            context.position.board[40 + rank] = matched.group(7)
            context.position.board[30 + rank] = matched.group(8)
            context.position.board[20 + rank] = matched.group(9)
            context.position.board[10 + rank] = matched.group(10)

            return '----Loopback---->'

        # ----[START:wdoor+floodgate-300-10F+e-gov-vote-kifuwarabe+Kristallweizen-Core2Duo-P7450+20211105220005]----> 対局合意成立
        #            ------------------------------------------------------------------------------------------
        #            1. game_id
        matched = self._start_pattern.match(line)
        if matched:
            start_game_id = matched.group(1)
            if context.game_id == start_game_id:
                self.on_start(context)
                return '----Start---->'
            else:
                raise ValueError(
                    f'GameIdが一致しませんでした GameId:{context.game_id} Start:{start_game_id}')

        log_output.display_and_log_internal(
            f"[DEBUG] Unknown line=[{line}]")
        return '----Loopback---->'


# Test
# python.exe -m floodgate_chat.client_state_diagram_d.game_summary_state
if __name__ == "__main__":
    context = Context()
    state = GameSummaryState()

    line = 'Game_ID:wdoor+floodgate-300-10F+Yss1000k+e-gov-vote-kifuwarabe+20211103193002'
    edge_name = state.leave(context, line)
    if edge_name == '----GameId---->':
        print('.', end='')
    else:
        print('f', end='')

    line = 'P1-KY-KE-GI-KI-OU-KI-GI-KE-KY'
    edge_name = state.leave(context, line)
    if edge_name == '----BeginPosRow---->':
        print('.', end='')
    else:
        print('f', end='')

    line = 'START:wdoor+floodgate-300-10F+e-gov-vote-kifuwarabe+Kristallweizen-Core2Duo-P7450+20211105220005'
    edge_name = state.leave(context, line)
    if edge_name == '----Start---->':
        print('.', end='')
    else:
        print('f', end='')
