import socket
from config import SERVER_HOST, SERVER_PORT, MESSAGE_SIZE
from scripts.logger import LogOutput, logger


class ClientSocket():

    def __init__(self):
        self._sock = None

    def set_up(self):
        # initialize TCP socket
        self._sock = socket.socket()

    def connect(self):
        # connect to the server
        print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
        self._sock.connect((SERVER_HOST, SERVER_PORT))
        print("[+] Connected.")

    def receive_text_block(self):
        """一行ずつではなく複数行を一気に受け取ることもある"""

        return self._sock.recv(MESSAGE_SIZE).decode()

    def send_line(self, line):
        """末尾に \n を付けてください"""
        global client_socket
        global logger

        # 1. Change Newline (Windows to CSA Protocol)
        if line.endswith('\r\n'):
            # ここは通らないと思う
            print('1. Change Newline (Windows to CSA Protocol)')
            line = line.rstrip('\r\n')
            line = f"{line}\n"
        elif line.endswith('\n'):
            print('1. Newline Ok')
        else:
            # コマンドラインから打鍵したときは、改行が付いていません
            print('1. Line without newline')
            line = f"{line}\n"

        # Send to server
        # テストのときは _sock が None になっているので無視します
        if not(self._sock is None):
            # ConnectionAbortedError といった例外を投げる
            self._sock.send(line.encode())

        s = LogOutput.format_send(line)

        # Display
        print(s)

        # Log
        logger.write(s)
        logger.flush()


client_socket = ClientSocket()
