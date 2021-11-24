class Context():
    def __init__(self):
        self._user_name = ''
        self._game_id = ''
        self._my_turn = ''
        self._current_turn = ''

    @property
    def user_name(self):
        """ログインユーザー名"""
        return self._user_name

    @user_name.setter
    def user_name(self, val):
        self._user_name = val

    @property
    def game_id(self):
        """初期局面概要で送られてくるゲームID"""
        return self._game_id

    @game_id.setter
    def game_id(self, val):
        self._game_id = val

    @property
    def my_turn(self):
        """自分の手番符号"""
        return self._my_turn

    @my_turn.setter
    def my_turn(self, val):
        self._my_turn = val

    @property
    def current_turn(self):
        return self._current_turn

    @current_turn.setter
    def current_turn(self, val):
        self._current_turn = val
