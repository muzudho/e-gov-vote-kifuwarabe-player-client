import re
from scripts.position import Position


class LoggedInState():

    def __init__(self):
        # Format: `Game_ID:<GameId>`
        # Example: `Game_ID:wdoor+floodgate-300-10F+Yss1000k+e-gov-vote-kifuwarabe+20211103193002`
        self._game_id_pattern = re.compile(r'^Game_ID:([0-9A-Za-z_+-]+)$')
        self._game_id = ''

        # 先手、後手プレイヤー名判定
        # Format: `Name<SenteOrGote>:<PlayerName>`
        # Example: `Name+:John`
        # Example: `Name-:e-gov-vote-kifuwarabe`
        self._player_name_pattern = re.compile(
            r'^Name([+-]):([0-9A-Za-z_-]+)$')
        # プレイヤー名 [未使用, 先手プレイヤー名, 後手プレイヤー名]
        self._player_names = ['', '', '']

        # わたしの手番
        # Format: `Your_Turn:<Turn>`
        # Example: `Your_Turn:+`
        self._my_turn_pattern = re.compile(
            r'^Your_Turn:([+-])$')
        self._my_turn = ''

        # 開始局面での手番
        # Format: `To_Move:<Turn>`
        # Example: `To_Move:+`
        self._startpos_turn_pattern = re.compile(
            r'^To_Move:([+-])$')
        self._startpos_turn = ''

        # Format: `START:<GameID>`
        # Example: `START:wdoor+floodgate-300-10F+e-gov-vote-kifuwarabe+Kristallweizen-Core2Duo-P7450+20211105220005`
        self._start_pattern = re.compile(r'^START:([0-9A-Za-z_+-]+)$')
        self._start_game_id = ''

        # 開始局面の各行
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
        self._begin_pos_row_pattern = re.compile(
            r"^P(\d)(.{3})(.{3})(.{3})(.{3})(.{3})(.{3})(.{3})(.{3})(.{3})$")

        self._position = Position()

    @property
    def name(self):
        return "<LoggedInState/>"

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

    def parse_line(self, line):

        # 初期局面終了
        if line == 'END Game_Summary':
            return '<LoggedInState.EndGameSummary/>'

        # 先手、後手プレイヤー名
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

            return '<LoggedInState.Turn/>'

        # 自分のターン
        matched = self._my_turn_pattern.match(line)
        if matched:
            self._my_turn = matched.group(1)
            return '<LoggedInState.MyTurn/>'

        # 開始局面のターン
        matched = self._startpos_turn_pattern.match(line)
        if matched:
            self._startpos_turn = matched.group(1)
            return '<LoggedInState.StartPosTurn/>'

        # Game_ID
        matched = self._game_id_pattern.match(line)
        if matched:
            # ログイン成功
            self._game_id = matched.group(1)
            return '<LoggedInState.GameId/>'

        # 開始局面の各行
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

            return '<Position.BeginPosRow/>'

        # START
        matched = self._start_pattern.match(line)
        if matched:
            # 対局合意成立
            self._start_game_id = matched.group(1)
            return '<LoggedInState.Start/>'

        return '<LoggedInState.Unknown>'
