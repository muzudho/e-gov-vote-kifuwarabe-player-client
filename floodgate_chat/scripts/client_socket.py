import socket
from config import SERVER_HOST, SERVER_PORT, MESSAGE_SIZE
from app import Logger, app


class ClientSocket():

    def __init__(self):
        self._sock = None

    def set_up(self):
        # initialize TCP socket
        self._sock = socket.socket()

    def connect(self):
        # connect to the server
        app.log.write_by_internal(
            f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
        self._sock.connect((SERVER_HOST, SERVER_PORT))
        app.log.write_by_internal("[+] Connected.")

    def receive_text_block(self):
        """一行ずつではなく複数行を一気に受け取ることもある"""
        return self._sock.recv(MESSAGE_SIZE).decode()

    def send_line(self, line):
        """末尾に \n を付けてください"""
        global client_socket

        if line.endswith('\n'):
            # ここを通るように目指してください
            # print('1. Newline Ok')
            pass
        # Change Newline (Windows to CSA Protocol)
        elif line.endswith('\r\n'):
            # ここは通らないと思う
            app.log.write_by_internal(
                '[WARNING] Change Newline (Windows to CSA Protocol)')
            line = line.rstrip('\r\n')
            line = f"{line}\n"
        else:
            # コマンドラインから打鍵したときは、改行が付いていません
            app.log.write_by_internal('[WARNING] Line without newline')
            line = f"{line}\n"

        # Send to server
        # テストのときは _sock が None になっているので無視します
        if not(self._sock is None):
            # ConnectionAbortedError といった例外を投げる
            self._sock.send(line.encode())

        s = Logger.format_send(line)

        # Display
        print(s)

        # Log
        app.log.write(s)
        app.log.flush()


client_socket = ClientSocket()
