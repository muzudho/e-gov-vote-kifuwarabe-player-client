from scripts.client_state.none_state import NoneState
from scripts.client_state.logged_in_state import LoggedInState
from scripts.client_state.game_state import GameState
from scripts.log_output import log_output


def SplitTextBlock(text_block):
    """受信したテキストブロックを行の配列にして返します"""
    lines = text_block.split('\n')

    # 例えば 'abc\n' を '\n' でスプリットすると 'abc' と '' になって、
    # 最後に空文字列ができます。これは無視します
    if lines[len(lines)-1] == '':
        lines = lines[:-1]

    return lines


class ClientP():
    def __init__(self):
        self._state = NoneState()
        self._user_name = ''
        self._game_id = ''
        self._start_game_id = ''
        self._my_turn = ''
        self._current_turn = ''

        def none_func():
            pass

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
        return self._agree_func

    @agree_func.setter
    def agree_func(self, func):
        self._agree_func = func

    def parse_line(self, line):
        result = self._state.parse_line(line)
        log_output.display_and_log_internal(
            f"[DEBUG] state=[{self._state.name}] result=[{result}]")

        if self._state.name == '<NoneState/>':
            if result == '<NoneState.LoginOk/>':
                # ログインした

                # 読み取った情報の記憶
                self._user_name = self._state.user_name

                # 次のステートへ引継ぎ
                next_state = LoggedInState()
                self._state = next_state

        elif self._state.name == '<LoggedInState/>':
            if result == '<LoggedInState.GameId/>':
                # Game ID を取得
                self._game_id = self._state.game_id
            elif result == '<LoggedInState.EndGameSummary/>':
                # 初期局面終了
                # 常に AGREE を返します
                self._agree_func()
            elif result == '<LoggedInState.Start/>':
                # 対局成立
                self._start_game_id = self._state.start_game_id

                # 読み取った情報の記憶
                self._my_turn = self._state.my_turn
                self._current_turn = self._state.startpos_turn

                # 次のステートへ引継ぎ
                next_state = GameState()
                next_state.position = self._state.position
                next_state.player_names = self._state.player_names
                self._state = next_state

        elif self._state.name == '<GameState/>':
            if result == '<Position.Move/>':
                # 指し手を反映した
                # 盤表示
                text = self.state.position.formatBoard()
                log_output.display_and_log_internal(text)

            elif result == '<Position.Win/>':
                # 勝ち
                s = f"""+----------+
|    WIN   |
+----------+
"""
                log_output.display_and_log_internal(s)

            elif result == '<Position.Lose/>':
                # 負け
                s = f"""+----------+
|   LOSE   |
+----------+
"""
                log_output.display_and_log_internal(s)

        else:
            pass
