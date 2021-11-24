import time
from floodgate_chat.client_state_diagram_d.border_state import LoginChoice
from floodgate_chat.client_state_diagram_d.logged_in_state import LoggedInChoice
from floodgate_chat.client_state_diagram_d.game_state import GameState
from floodgate_chat.scripts.log_output import log_output
from floodgate_chat.scripts.client_socket import client_socket
from dynamodb.e_gov_bestmove import get_bestmove
from dynamodb.e_gov_delete_bestmove_table import delete_bestmove_table
from dynamodb.e_gov_create_bestmove_table import create_bestmove_table


def SplitTextBlock(text_block):
    """受信したテキストブロックを行の配列にして返します"""
    lines = text_block.split('\n')

    # 例えば 'abc\n' を '\n' でスプリットすると 'abc' と '' になって、
    # 最後に空文字列ができます。これは無視します
    if lines[len(lines)-1] == '':
        lines = lines[:-1]

    return lines


class ClientStateDiagram():
    def __init__(self):
        # 初期状態
        self._state = self.create_login_choice()

        self._user_name = ''
        self._game_id = ''
        self._start_game_id = ''

        # 自分の手番符号
        self._my_turn = ''

        self._current_turn = ''

        def none_func():
            pass

        # アグリーを返すコールバック関数
        self._agree_func = none_func

    @property
    def state(self):
        return self._state

    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, val):
        self._user_name = val

    @property
    def my_turn(self):
        return self._my_turn

    @my_turn.setter
    def my_turn(self, val):
        self._my_turn = val

    @property
    def current_turn(self):
        return self._current_turn

    @current_turn.setter
    def current_turn(self, val):
        self._current_turn = val

    @property
    def agree_func(self):
        """アグリーを返すコールバック関数"""
        return self._agree_func

    @agree_func.setter
    def agree_func(self, func):
        self._agree_func = func

    def create_login_choice(self):
        """ステート生成"""
        self._state = LoginChoice()

        def on_ok():
            # 読み取った情報の記憶
            self._user_name = self._state.user_name
            # 次のステートへ引継ぎ
            self._state = self.create_logged_in_choice()

        self._state.on_ok = on_ok

    def create_logged_in_choice(self):
        """ステート生成"""
        state = LoggedInChoice()

        def on_game_id():
            """Game ID を取得した"""
            self._game_id = self._state.game_id

        self._state.on_game_id = on_game_id

        def on_end_game_summary():
            """初期局面情報取得した"""
            # 常に AGREE を返します
            self._agree_func()

        self._state.on_end_game_summary = on_end_game_summary

        def on_start():
            """対局成立した"""
            self._start_game_id = self._state.start_game_id

            # 読み取った情報の記憶
            self._my_turn = self._state.my_turn
            self._current_turn = self._state.startpos_turn

            # 次のステートへ引継ぎ
            game_state = self.create_game_state()

            # テーブルを削除します
            try:
                delete_bestmove_table()

                # 時間間隔を開けてみる
                time.sleep(5)
            except Exception as e:
                log_output.display_and_log_internal(
                    f"(Err.158) テーブル削除できなかった [{e}]")

            # テーブルを作成します
            try:
                create_bestmove_table()

                # 時間間隔を開けてみる
                time.sleep(5)
            except Exception as e:
                log_output.display_and_log_internal(
                    f"(Err.163) テーブル作成できなかった [{e}]")

            if self._my_turn == self._current_turn:
                # 初手を考えます
                log_output.display_and_log_internal(f"(175) 初手を考えます")
                m = game_state.go_func()
                client_socket.send_line(f'{m}\n')
                log_output.display_and_log_internal(
                    f"(178) 初手を指します m=[{m}]")

            self._state = game_state

        self._state.on_start = on_start

        return state

    def create_game_state(self):
        """ステート生成"""
        game_state = GameState()
        game_state.position = self._state.position
        game_state.player_names = self._state.player_names
        game_state.my_turn = self._my_turn

        # コールバック関数の初期設定
        def go_func():

            # a. 手番が回ってきた直後の待ち時間
            init_sec = 20  # 10, 20
            # b. 投票が無かったときの追加の待ち時間
            interval_sec = 10  # 5, 10
            # c. 投票を待つ回数
            tryal_max = 34  # 70, 34
            # サンプル
            #  a,  b,  c なら、 c*b +  a
            # 10,  5, 70 なら、70*5 + 10 = 360 = 6分
            # 20, 10, 34 なら、34*10 +20 = 360 = 6分

            # 手番が回ってきた直後の待ち時間
            time.sleep(init_sec)

            tryal_count = 0
            while True:
                m = get_bestmove()

                if not(m is None):
                    # 投票が溜まってたので指します
                    log_output.display_and_log_internal(
                        f"投票が溜まってたので指します [{m}]")
                    return m

                if tryal_max < tryal_count:
                    # 投了しよ
                    log_output.display_and_log_internal(
                        f"投票が無いので投了しよ tryal_count = [{m}]")
                    return '%TORYO'

                # 投票が無かったときの追加の待ち時間
                time.sleep(interval_sec)
                tryal_count += 1

        game_state.go_func = go_func

        def on_move():
            """指し手を反映した"""
            # テーブルを削除します
            try:
                delete_bestmove_table()

                # 時間間隔を開けてみる
                time.sleep(5)
            except Exception as e:
                log_output.display_and_log_internal(
                    f"(Err.178) テーブル削除できなかった [{e}]")
            # テーブルを作成します
            try:
                create_bestmove_table()

                # 時間間隔を開けてみる
                time.sleep(5)
            except Exception as e:
                log_output.display_and_log_internal(
                    f"(Err.183) テーブル作成できなかった [{e}]")

            # 盤表示
            text = self.state.position.formatBoard()
            log_output.display_and_log_internal(text)

        game_state.on_move = on_move

        def on_win():
            """勝ち"""
            s = f"""+----------+
|    WIN   |
+----------+
"""
            log_output.display_and_log_internal(s)

        game_state.on_win = on_win

        def on_lose():
            """負け"""
            s = f"""+----------+
|   LOSE   |
+----------+
"""
            log_output.display_and_log_internal(s)

        game_state.on_lose = on_lose

        return game_state

    def forward(self, line):
        """状態遷移します
        Parameters
        ----------
        str : line
            入力文字列（末尾に改行なし）
        """

        # ここで状態遷移します
        edge = self._state.forward(line)

        log_output.display_and_log_internal(
            f"[DEBUG] state=[{self._state.name}] edge=[{edge}]")
