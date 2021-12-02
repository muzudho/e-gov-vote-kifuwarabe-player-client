import re
from app import app
from state_machine_py.abstract_state import AbstractState
from context import Context


class ListenState(AbstractState):
    def __init__(self):
        super().__init__()

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

    @property
    def name(self):
        return "[Listen]"

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

        # ----[END Game_Summary]---->
        #      ----------------
        #      1. 対局条件通知終了
        if line == 'END Game_Summary':
            self.on_agree(context)
            return '----Agree---->'

        app.log.write_by_internal(
            f"[DEBUG] Unknown line=[{line}]")
        return '----Loopback---->'

    def on_game_id(self, context):
        """----GameId---->時"""
        pass

    def on_agree(self, context):
        """----Agree---->"""
        pass


# Test
# python.exe -m floodgate_client.layer1_transition_map.listen
if __name__ == "__main__":
    app.log.set_up()
    context = Context()
    state = ListenState()

    line = 'Game_ID:wdoor+floodgate-300-10F+Yss1000k+e-gov-vote-kifuwarabe+20211103193002'
    edge_name = state.leave(context, line)
    if edge_name == '----GameId---->':
        app.log.write_by_internal('.', end='')
    else:
        app.log.write_by_internal('f', end='')

    line = 'P1-KY-KE-GI-KI-OU-KI-GI-KE-KY'
    edge_name = state.leave(context, line)
    if edge_name == '----BeginPosRow---->':
        app.log.write_by_internal('.', end='')
    else:
        app.log.write_by_internal('f', end='')

    line = 'START:wdoor+floodgate-300-10F+e-gov-vote-kifuwarabe+Kristallweizen-Core2Duo-P7450+20211105220005'
    edge_name = state.leave(context, line)
    if edge_name == '----Start---->':
        app.log.write_by_internal('.', end='')
    else:
        app.log.write_by_internal('f', end='')
