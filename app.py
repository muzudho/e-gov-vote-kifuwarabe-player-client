from scripts.logger import Logger


class App():
    """グローバル変数のようなもの"""

    def __init__(self):
        self._log = Logger()

    @property
    def log(self):
        """ロガー"""
        return self._log

    @log.setter
    def log(self, func):
        self._log = func


app = App()
