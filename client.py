import sys
import signal
from threading import Thread
from floodgate_chat.client_state_diagram_d.diagram import Diagram, SplitTextBlock
from floodgate_chat.scripts.log_output import log_output
from floodgate_chat.scripts.client_socket import client_socket
from config import CLIENT_USER, CLIENT_PASS


class Client():
    def __init__(self):
        self._state_diagram = None

    @property
    def state_diagram(self):
        return self._state_diagram

    def set_up(self):
        global log_output

        print("# Set up")
        log_output.set_up()

        self._state_diagram = Diagram()

        # Implement all handlers
        def __agree_func():
            client_socket.send_line(
                f"AGREE {self.state_diagram.context.game_id}\n")

        self.state_diagram.agree_func = __agree_func

    def clean_up(self):
        print("# Clean up")

        # Close log file
        if not(log_output is None):
            log_output.clean_up()

    def run(self):
        """自動対話"""
        global client_socket

        client_socket.set_up()
        client_socket.connect()

        # Login
        client_socket.send_line(f"LOGIN {CLIENT_USER} {CLIENT_PASS}\n")

        # このスレッドはコンピューターが自動入力するためのものです
        # make a thread that listens for messages to this client & print them
        thr = Thread(target=self.listen_for_messages)
        # make the thread daemon so it ends whenever the main thread ends
        thr.daemon = True
        # start the thread
        thr.start()

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
            client_socket.send_line(to_send)

    def listen_for_messages(self):
        """コンピューターの動き"""
        global client_socket

        while True:
            text_block = client_socket.receive_text_block()

            # 1. 空行は無限に送られてくるので無視
            if text_block == '':
                continue

            log_output.display_and_log_receive(text_block)

            # 受信したテキストブロックを行の配列にして返します
            lines = SplitTextBlock(text_block)
            for line in lines:

                log_output.display_and_log_receive(line)

                # 処理は Diagram に委譲します
                next_state_name = self._state_diagram.leave(line)
                self._state_diagram.arrive(next_state_name)


def main():
    def sigterm_handler(_signum, _frame) -> None:
        sys.exit(1)

    # 強制終了のシグナルを受け取ったら、強制終了するようにします
    signal.signal(signal.SIGTERM, sigterm_handler)
    client = Client()
    client.set_up()

    try:
        client.run()
    finally:
        # 強制終了のシグナルを無視するようにしてから、クリーンアップ処理へ進みます
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        client.clean_up()
        # 強制終了のシグナルを有効に戻します
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        signal.signal(signal.SIGINT, signal.SIG_DFL)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    sys.exit(main())
