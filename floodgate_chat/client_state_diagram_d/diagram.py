import time
from floodgate_chat.client_state_diagram_d.context import Context
from floodgate_chat.client_state_diagram_d.mapping import connection_dict
from floodgate_chat.client_state_diagram_d.none_state import NoneState
from floodgate_chat.client_state_diagram_d.game_summary_state import GameSummaryState
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


class Diagram():
    def __init__(self):
        # グローバル変数みたいなもん
        self._context = Context()

        self._state_creators = {
            "": self.create_none_state,  # 初期値
            "[Login].<Login>": self.create_none_state,
            "[GameSummary]": self.create_game_summary_state,
            "[Game]": self.create_game_state
        }

        # 初期状態
        self._state = self._state_creators[""]()

        def none_func():
            pass

        # アグリーを返すコールバック関数
        self._agree_func = none_func

        # 指し手を返すコールバック関数
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

        self._go_func = go_func

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, val):
        self._context = val

    @property
    def state(self):
        return self._state

    @property
    def agree_func(self):
        """アグリーを返すコールバック関数"""
        return self._agree_func

    @agree_func.setter
    def agree_func(self, func):
        self._agree_func = func

    @property
    def go_func(self):
        """指し手を返すコールバック関数"""
        return self._go_func

    @go_func.setter
    def go_func(self, func):
        self._go_func = func

    def create_none_state(self):
        """ステート生成"""
        state = NoneState()

        def on_ok(_context):
            pass

        state.on_ok = on_ok
        return state

    def create_game_summary_state(self):
        """ステート生成"""
        state = GameSummaryState()

        def on_game_id(context):
            """Game ID を取得した"""
            pass

        state.on_game_id = on_game_id

        def on_end_game_summary(context):
            """初期局面情報取得した"""
            # 常に AGREE を返します
            self._agree_func()

        state.on_end_game_summary = on_end_game_summary

        def on_start(context):
            """対局成立した"""
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

            if self.context.my_turn == self.context.current_turn:
                # 初手を考えます
                log_output.display_and_log_internal(f"(175) 初手を考えます")
                m = self.go_func()
                client_socket.send_line(f'{m}\n')
                log_output.display_and_log_internal(
                    f"(178) 初手を指します m=[{m}]")

            # 次のステートへ引継ぎ
            self._state = self._state_creators["[Game]"]()

        state.on_start = on_start

        return state

    def create_game_state(self):
        """ステート生成"""
        state = GameState()

        def on_move(context):
            """指し手"""
            # 相手の指し手だったら、自分の指し手を入力する番になります
            if self.context.current_turn != self.context.my_turn:
                print(
                    f"自分の手番が回ってきました。考えます: current_turn=[{self.context.current_turn}] my_turn=[{self.context.my_turn}]")
                m = self.go_func()
                client_socket.send_line(f'{m}\n')
                log_output.display_and_log_internal(
                    f"(191) 自分の手番で指した m=[{m}]")

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
            text = self.context.position.formatBoard()
            log_output.display_and_log_internal(text)

        state.on_move = on_move

        def on_win(context):
            """勝ち"""
            s = f"""+----------+
|    WIN   |
+----------+
"""
            log_output.display_and_log_internal(s)

        state.on_win = on_win

        def on_lose(context):
            """負け"""
            s = f"""+----------+
|   LOSE   |
+----------+
"""
            log_output.display_and_log_internal(s)

        state.on_lose = on_lose

        return state

    def leave(self, line):
        """次の辺の名前を返します
        Parameters
        ----------
        str : line
            入力文字列（末尾に改行なし）

        Returns
        -------
        str
            次の状態の名前
        """

        edge_name = self._state.leave(self._context, line)

        # さっき去ったステートの名前と、今辿っているエッジの名前
        key = f"{self._state.name}{edge_name}"

        if key in connection_dict:
            return connection_dict[key]

        log_output.display_and_log_internal(
            f"[DEBUG] state=[{self._state.name}] edge=[{edge_name}]")

        return None

    def arrive(self, next_state_name):
        """次の節の名前を返します
        Parameters
        ----------
        str : next_state_name
            次の状態の名前

        Returns
        -------
        str
            節の名前
        """

        if next_state_name == "[GameSummary]":
            # 次のステートへ引継ぎ
            self._state = self._state_creators["[GameSummary]"]()
        else:
            # Error
            raise ValueError(f"Next sate [{next_state_name}] is None")