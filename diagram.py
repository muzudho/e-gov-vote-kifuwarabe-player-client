import sys
import signal
from threading import Thread
from config import IS_RECONNECT_WHEN_CONNECTION_ABORT
from app import app
from state_machine_py.state_machine import StateMachine
from context import Context
from floodgate_client.transition_dict import transition_dict
from floodgate_client.state_creator_dict import state_creator_dict


def SplitTextBlock(text_block):
    """受信したテキストブロックを行の配列にして返します"""
    lines = text_block.split('\n')

    # 例えば 'abc\n' を '\n' でスプリットすると 'abc' と '' になって、
    # 最後に空文字列ができます。これは無視します
    if lines[len(lines)-1] == '':
        lines = lines[:-1]

    return lines


class Diagram():
    def __init__(self, context):
        self._state_machine = StateMachine(
            context=context, state_creator_dict=state_creator_dict, transition_dict=transition_dict)

        # デバッグ情報出力
        self._state_machine.verbose = True

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

        # （強制的に）ステートマシンを初期状態に戻します。 leave は行いません
        interrupt_line = self.state_machine.arrive("[Init]")
        app.log.write_by_internal(
            f"[E-GOV] arrive [init] おわり (init.py init 67)")

        # いきなり [pass_on割り込み] あるかもしれないのでループ
        while interrupt_line:
            app.log.write_by_internal(
                f"[E-GOV] interrupt_line={interrupt_line} (diagram.py 71)")

            next_state_name, transition_key = self.state_machine.leave(
                interrupt_line)

            interrupt_line = self.state_machine.arrive(
                next_state_name)

            app.log.write_by_internal(
                f"[E-GOV] interrupt_line={interrupt_line} (init.py init 80)")

        # 以降、コマンドの受信をトリガーにして状態を遷移します
        thr = Thread(target=self.listen_for_messages)
        thr.daemon = True
        thr.start()

    def listen_for_messages(self):
        """コンピューターの動き"""

        try:
            while True:
                app.log.write_by_internal(
                    f"[E-GOV] 受信ループ開始 (init.py init 93)")

                text_block = self._state_machine.context.client_socket.receive_text_block()

                # 1. 空行は無限に送られてくるので無視
                if text_block == '':
                    continue

                app.log.write_by_receive(text_block)

                # 受信したテキストブロックを行の配列にして返します
                lines = SplitTextBlock(text_block)
                for line in lines:

                    app.log.write_by_internal(
                        f"[E-GOV] line={line} (init.py init 105)")

                    app.log.write_by_receive(line)

                    # 遷移処理
                    interrupt_line = line
                    while interrupt_line:
                        app.log.write_by_internal(
                            f"[E-GOV] interrupt_line={interrupt_line} (diagram.py 110)")

                        next_state_name, transition_key = self.state_machine.leave(
                            line)

                        interrupt_line = self.state_machine.arrive(
                            next_state_name)

                        app.log.write_by_internal(
                            f"[E-GOV] interrupt_line={interrupt_line} (init.py init 119)")

                    app.log.write_by_internal(
                        f"[E-GOV] 割り込みループ抜けた (init.py init 122)")

                app.log.write_by_internal(
                    f"[E-GOV] 入力ループ抜けた (init.py init 128)")

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


def main():
    def sigterm_handler(_signum, _frame) -> None:
        sys.exit(1)

    # 強制終了のシグナルを受け取ったら、強制終了するようにします
    signal.signal(signal.SIGTERM, sigterm_handler)

    context = Context()

    diagram = Diagram(context)

    # Implement all handlers
    def __agree_func():
        context.client_socket.send_line(
            f"AGREE {diagram.state_machine.context.game_id}\n")

    # 後付け
    context.agree_func = __agree_func

    try:
        diagram.run()
    finally:
        # 強制終了のシグナルを無視するようにしてから、クリーンアップ処理へ進みます
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        diagram.clean_up()
        # 強制終了のシグナルを有効に戻します
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        signal.signal(signal.SIGINT, signal.SIG_DFL)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    sys.exit(main())
