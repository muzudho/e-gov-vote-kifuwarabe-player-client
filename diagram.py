import sys
import signal
from threading import Thread
from config import IS_RECONNECT_WHEN_CONNECTION_ABORT
from app import app
from state_machine_d.state_machine import StateMachine
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

    @property
    def state_machine(self):
        """ダイアグラム"""
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

        # （強制的に）ステートマシンを初期状態に戻します。 leave は行いません
        self.state_machine.arrive("[Init]")

        # 以降、コマンドの受信をトリガーにして状態を遷移します
        thr = Thread(target=self.listen_for_messages)
        thr.daemon = True
        thr.start()

    def listen_for_messages(self):
        """コンピューターの動き"""

        try:
            while True:
                text_block = self._state_machine.context.client_socket.receive_text_block()

                # 1. 空行は無限に送られてくるので無視
                if text_block == '':
                    continue

                app.log.write_by_receive(text_block)

                # 受信したテキストブロックを行の配列にして返します
                lines = SplitTextBlock(text_block)
                for line in lines:

                    app.log.write_by_receive(line)

                    # 処理は Diagram に委譲します
                    next_state_name, transition_key = self.state_machine.leave(
                        line)
                    app.log.write_by_internal(
                        f"[DEBUG] Transition {transition_key} {next_state_name} (diagram.py 108)")

                    self.state_machine.arrive(next_state_name)

        except ConnectionAbortedError as e:
            # floodgate に切断されたときとか
            app.log.write_by_internal(
                f"(Err.51) 接続が破棄された [{e}]")

            # 接続のタイミングによっては状態遷移が壊れるけど（＾～＾）
            if IS_RECONNECT_WHEN_CONNECTION_ABORT:
                # ログイン、スレッド生成からやり直すので、このスレッドは終了してください
                self.init()

    def clean_up(self):
        print("# Clean up")

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
