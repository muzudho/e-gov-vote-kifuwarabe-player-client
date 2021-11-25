import socket
from config import SERVER_HOST, SERVER_PORT, MESSAGE_SIZE
from scripts.logger import Logger, logger


class ClientSocket():

    def __init__(self):
        self._sock = None

    def set_up(self):
        # initialize TCP socket
        self._sock = socket.socket()

    def connect(self):
        global logger
        # connect to the server
        logger.write_by_internal(
            f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
        self._sock.connect((SERVER_HOST, SERVER_PORT))
        logger.write_by_internal("[+] Connected.")

    def receive_text_block(self):
        """一行ずつではなく複数行を一気に受け取ることもある"""
        return self._sock.recv(MESSAGE_SIZE).decode()

    def send_line(self, line):
        """末尾に \n を付けてください"""
        global client_socket
        global logger

        if line.endswith('\n'):
            # ここを通るように目指してください
            # print('1. Newline Ok')
            pass
        # Change Newline (Windows to CSA Protocol)
        elif line.endswith('\r\n'):
            # ここは通らないと思う
            logger.write_by_internal(
                '[WARNING] Change Newline (Windows to CSA Protocol)')
            line = line.rstrip('\r\n')
            line = f"{line}\n"
        else:
            # コマンドラインから打鍵したときは、改行が付いていません
            logger.write_by_internal('[WARNING] Line without newline')
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
        logger.write(s)
        logger.flush()


client_socket = ClientSocket()
