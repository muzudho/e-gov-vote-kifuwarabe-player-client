class AbstractState():
    def __init__(self):
        def on_none(context):
            pass

        self._on_entry = on_none
        self._on_exit = on_none

    @property
    def on_entry(self):
        """Entry時のコールバック関数"""
        return self._on_entry

    @on_entry.setter
    def on_entry(self, func):
        self._on_entry = func

    @property
    def on_exit(self):
        """Exit時のコールバック関数"""
        return self._on_exit

    @on_exit.setter
    def on_exit(self, func):
        self._on_exit = func
