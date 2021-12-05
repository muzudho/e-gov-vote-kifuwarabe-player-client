from threading import Thread
from config import IS_RECONNECT_WHEN_CONNECTION_ABORT
from app import app
from state_machine_py.state_machine import StateMachine
from floodgate_client_state.transition_dict import transition_dict
from floodgate_client_state.state_creator_dict import state_creator_dict
from context import Context


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
        context = Context()

        self._state_machine = StateMachine(
            context=context, state_creator_dict=state_creator_dict, transition_dict=transition_dict)

        # Implement all handlers
        def __agree_func():
            context.client_socket.send_line(
                f"AGREE {self._state_machine.context.game_id}\n")

        # 後付け
        context.agree_func = __agree_func

        # デバッグ情報出力
        self._state_machine.verbose = True

        def __on_line(line):
            app.log.write_by_receive(line)

        self._state_machine.on_line = __on_line

    @property
    def state_machine(self):
        """状態遷移マシン"""
        return self._state_machine

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
                break

            # 指し手を人力で入力するとき

            # Send the message
            self._state_machine.context.client_socket.send_line(to_send)

    def init(self):
        """ダイアグラムを初期状態に戻します"""

        # ログを初期状態に戻します
        app.log.init()
        app.log.write_by_internal(
            f"初期状態に戻します (init.py init 62)")

        # 以降、コマンドの受信をトリガーにして状態を遷移します
        thr = Thread(target=self.listen_for_messages)
        thr.daemon = True
        thr.start()

    def listen_for_messages(self):
        """コンピューターの動き"""

        try:
            def __lines_getter():
                while True:
                    text_block = self._state_machine.context.client_socket.receive_text_block()

                    # FIXME 突然、空行が無限に送られてくるので無視。なんでだろう？
                    if text_block != '':
                        print('kara')
                        break

                app.log.write_by_receive(text_block)

                # 受信したテキストブロックを行の配列にして返します
                lines = SplitTextBlock(text_block)

                app.log.write_by_internal(f"[E-GOV] lines=[{lines}]")

                return lines

            # （強制的に）ステートマシンを初期状態に戻して、開始します
            self.state_machine.start("[Init]", __lines_getter)

        except ConnectionAbortedError as e:
            # floodgate に切断されたときとか
            app.log.write_by_internal(
                f"(Err.51) 接続が破棄された [{e}]")

            # 接続のタイミングによっては状態遷移が壊れるけど（＾～＾）
            if IS_RECONNECT_WHEN_CONNECTION_ABORT:
                # ログイン、スレッド生成からやり直すので、このスレッドは終了してください
                self.init()

    def clean_up(self):
        app.log.write_by_internal("# Clean up")

        # Close log file
        if not(app.log is None):
            app.log.clean_up()
