from threading import Thread
from state_machine_py.multiple_state_machine import MultipleStateMachine
from config import IS_RECONNECT_WHEN_CONNECTION_ABORT
from app import app
from floodgate.keywords import INIT, MACHINE_C, MACHINE_S, RECEIPT
from floodgate.client_state_machine.transition_dict import transition_dict as transition_dict_c
from floodgate.client_state_machine.state_creator_dict import state_creator_dict as state_creator_dict_c
from floodgate.client_state_machine.context import Context as ContextC
from floodgate.server_state_machine.transition_dict import transition_dict as transition_dict_s
from floodgate.server_state_machine.state_creator_dict import state_creator_dict as state_creator_dict_s
from floodgate.server_state_machine.context import Context as ContextS


def SplitTextBlock(text_block):
    """受信したテキストブロックを行の配列にして返します"""
    lines = text_block.split('\n')

    # 例えば 'abc\n' を '\n' でスプリットすると 'abc' と '' になって、
    # 最後に空文字列ができます。これは無視します
    if lines[len(lines)-1] == '':
        lines = lines[:-1]

    return lines


class MainDiagram():
    def __init__(self):
        self._multiple_state_machine = MultipleStateMachine()

        machine_c = self._multiple_state_machine.create_machine(
            MACHINE_C,
            context=ContextC(),
            state_creator_dict=state_creator_dict_c,
            transition_dict=transition_dict_c)
        machine_c.verbose = True  # デバッグ情報を出力します

        machine_s = self._multiple_state_machine.create_machine(
            MACHINE_S,
            context=ContextS(),
            state_creator_dict=state_creator_dict_s,
            transition_dict=transition_dict_s)
        machine_s.verbose = True  # デバッグ情報を出力します

        # Implement all handlers
        def __agree_func():
            machine_c.context.client_socket.send_line(
                f"AGREE {self._state_machine.context.game_id}\n")

        # 後付け
        machine_c.context.agree_func = __agree_func

        def __on_line(line):
            app.log.write_by_receive(line)

        machine_c.on_line = __on_line
        machine_s.on_line = __on_line

    @property
    def multiple_state_machine(self):
        """複数の状態遷移マシン"""
        return self._multiple_state_machine

    def run(self):
        """自動対話"""
        self.init()

        # このループは人間が入力するためのものです
        while True:
            # input message we want to send to the server
            # 末尾に改行は付いていません
            to_send = input()

            # a way to exit the program
            if to_send.lower() == 'q':
                # ステートマシーンを終了させます
                self._state_machine.terminate()
                break

            # 指し手を人力で入力するとき

            # Send the message
            self._state_machine.context.client_socket.send_line(to_send)

    def init(self):
        """ダイアグラムを初期状態に戻します"""

        # ログを初期状態に戻します
        app.log.init()
        app.log.write_by_internal(f"初期状態に戻します (init.py init 62)")

        self.init_cr()
        self.init_c()
        self.init_s()

    def init_cr(self):
        # 読取
        thr = Thread(target=self.work_of_machine_client_receive, daemon=True)
        thr.start()

    def init_c(self):
        # Client side
        thr = Thread(target=self.work_of_machine_c, daemon=True)
        thr.start()

    def init_s(self):
        # Server side
        thr = Thread(target=self.work_of_machine_s, daemon=True)
        thr.start()

    def work_of_machine_client_receive(self):
        try:
            while True:
                text_block = self._state_machine.context.client_socket.receive_text_block()

                # FIXME 突然、空行が無限に送られてくるので無視。なんでだろう？
                if text_block != '':
                    print('kara')
                    break

            app.log.write_by_receive(text_block)

            # 受信したテキストブロックを行の配列にして返します
            lines = SplitTextBlock(text_block)
            for line in lines:
                app.log.write_by_internal(f"[E-GOV] line=[{line}]")
                self.multiple_state_machine.machines[MACHINE_C].input_queue.put(
                    line)

        except ConnectionAbortedError as e:
            # floodgate に切断されたときとか
            app.log.write_by_internal(
                f"[ClientReceive] 接続が破棄された e={e}")

            # 接続のタイミングによっては状態遷移が壊れるけど（＾～＾）
            if IS_RECONNECT_WHEN_CONNECTION_ABORT:
                # ログイン、スレッド生成からやり直すので、このスレッドは終了してください
                self.init_cr()

    def work_of_machine_c(self):
        try:
            # （強制的に）ステートマシンを初期状態から始めます
            self._multiple_state_machine.machines[MACHINE_C].start(INIT)
        except ConnectionAbortedError as e:
            # floodgate に切断されたときとか
            app.log.write_by_internal(
                f"[C] 接続が破棄された e={e}")

            # 接続のタイミングによっては状態遷移が壊れるけど（＾～＾）
            if IS_RECONNECT_WHEN_CONNECTION_ABORT:
                # ログイン、スレッド生成からやり直すので、このスレッドは終了してください
                self.init_c()

    def work_of_machine_s(self):
        try:
            # （強制的に）ステートマシンを初期状態から始めます
            self._multiple_state_machine.machines[MACHINE_S].start(RECEIPT)
        except ConnectionAbortedError as e:
            # floodgate に切断されたときとか
            app.log.write_by_internal(
                f"[S] 接続が破棄された e={e}")

            # 接続のタイミングによっては状態遷移が壊れるけど（＾～＾）
            if IS_RECONNECT_WHEN_CONNECTION_ABORT:
                # ログイン、スレッド生成からやり直すので、このスレッドは終了してください
                self.init_s()

    def clean_up(self):
        app.log.write_by_internal("# Clean up")

        # Close log file
        if not(app.log is None):
            app.log.clean_up()
