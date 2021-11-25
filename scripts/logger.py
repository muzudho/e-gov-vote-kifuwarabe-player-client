from datetime import datetime

LOG_FILE_NAME = 'client-chat.log'


class Logger():

    @classmethod
    def date_now(clazz):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def format_send(clazz, text):
        return f"[{Logger.date_now()}] < {text}\n"

    @classmethod
    def format_receive(clazz, text):
        return f"[{Logger.date_now()}] > {text}\n"

    @classmethod
    def format_internal(clazz, text):
        return f"[{Logger.date_now()}] : {text}\n"

    def __init__(self):
        self._file = None

    def set_up(self):
        self._file = open(LOG_FILE_NAME, "w", encoding="utf-8")

    def clean_up(self):
        # Close log file
        if not(self._file is None):
            self._file.close()

    def write(self, msg):
        self._file.write(msg)

    def flush(self):
        self._file.flush()

    def write_by_receive(self, text):
        """標準出力への印字と、ログへの書き込みを行います"""
        s = Logger.format_receive(text)

        # Display
        print(s, end='')

        # Log
        logger.write(s)
        logger.flush()

    def write_by_internal(self, text):
        """標準出力への印字と、ログへの書き込みを行います"""
        s = Logger.format_internal(text)

        # Display
        print(s)

        # Log
        logger.write(s)
        logger.flush()


logger = Logger()
