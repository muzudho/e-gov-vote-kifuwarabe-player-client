import time
from floodgate_chat.diagrams.client_state.none_state import NoneState
from floodgate_chat.diagrams.client_state.logged_in_state import LoggedInState
from floodgate_chat.diagrams.client_state.game_state import GameState
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


class ClientDiagram():
    def __init__(self):
        self._state = NoneState()
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

    def forward_by_line(self, line):

        # ここで状態遷移します
        result = self._state.forward_by_line(line)

        log_output.display_and_log_internal(
            f"[DEBUG] state=[{self._state.name}] result=[{result}]")

        # [無]状態
        if self._state.name == '<NoneState/>':
            # ログインした
            if result == '<NoneState.LoginOk/>':

                # 読み取った情報の記憶
                self._user_name = self._state.user_name

                # 次のステートへ引継ぎ
                next_state = LoggedInState()
                self._state = next_state

        # [ログイン済]状態
        elif self._state.name == '<LoggedInState/>':
            # Game ID を取得した
            if result == '<LoggedInState.GameId/>':
                self._game_id = self._state.game_id

            # 初期局面情報取得した
            elif result == '<LoggedInState.EndGameSummary/>':
                # 常に AGREE を返します
                self._agree_func()

            # 対局成立した
            elif result == '<LoggedInState.Start/>':
                self._start_game_id = self._state.start_game_id

                # 読み取った情報の記憶
                self._my_turn = self._state.my_turn
                self._current_turn = self._state.startpos_turn

                # 次のステートへ引継ぎ
                next_state = GameState()
                next_state.position = self._state.position
                next_state.player_names = self._state.player_names
                next_state.my_turn = self._my_turn

                # コールバック関数の初期設定
                def go_func():

                    # 投票中なので、10秒待ちます
                    time.sleep(10)

                    tryal_count = 0
                    while True:
                        m = get_bestmove()

                        if not(m is None):
                            # 投票が溜まってたので指します
                            log_output.display_and_log_internal(
                                f"投票が溜まってたので指します [{m}]")
                            return m

                        # 10回試せば 5*10 + 10 = 1分。 17回試せば 17*10 + 10 = 3分。
                        if 17 < tryal_count:
                            # 投了しよ
                            log_output.display_and_log_internal(
                                f"投票が無いので投了しよ tryal_count = [{m}]")
                            return '%TORYO'

                        # 投票が 0件 だったら、入力中かも知れないので、5秒待ちます
                        time.sleep(5)
                        tryal_count += 1

                next_state.go_func = go_func

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
                    m = next_state.go_func()
                    client_socket.send_line(f'{m}\n')
                    log_output.display_and_log_internal(
                        f"(178) 初手を指します m=[{m}]")

                self._state = next_state

        # [対局]状態
        elif self._state.name == '<GameState/>':
            # 指し手を反映した
            if result == '<Position.Move/>':

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

            # 勝ち
            elif result == '<Position.Win/>':
                s = f"""+----------+
|    WIN   |
+----------+
"""
                log_output.display_and_log_internal(s)

            # 負け
            elif result == '<Position.Lose/>':
                s = f"""+----------+
|   LOSE   |
+----------+
"""
                log_output.display_and_log_internal(s)

        else:
            pass
