from datetime import datetime

LOG_DIRECTORY = 'logs/'
LOG_FILE_STEM = 'client-chat-'
LOG_FILE_EXTENSION = '.log'


class Logger():

    @classmethod
    def date_now(clazz):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def file_name_date_now(clazz):
        return datetime.now().strftime('%Y%m%d-%H%M%S')

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
        self._file_name = None

        def none_func():
            pass

        # ファイルクローズ時
        self._on_file_close = none_func

    @property
    def on_file_close(self):
        """ファイルクローズ時"""
        return self._on_file_close

    @on_file_close.setter
    def on_file_close(self, func):
        self._on_file_close = func

    def clean_up(self):
        # Close log file
        if not(self._file is None):
            self._file.close()

    def init(self):
        """ログファイルを新規に用意します"""
        # 以前にファイルを作っていれば、解放します
        if not(self._file is None):
            self._file.close()
            # AWS S3 にアップロードするなどの処理も入れたい

        # ファイル名
        self._file_name = f"{LOG_DIRECTORY}{LOG_FILE_STEM}{Logger.file_name_date_now()}{LOG_FILE_EXTENSION}"

        # ファイルオープン
        self._file = open(
            self._file_name, "w", encoding="utf-8")

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
        self.write(s)
        self.flush()

    def write_by_internal(self, text):
        """標準出力への印字と、ログへの書き込みを行います"""
        s = Logger.format_internal(text)

        # Display
        print(s)

        # Log
        self.write(s)
        self.flush()
