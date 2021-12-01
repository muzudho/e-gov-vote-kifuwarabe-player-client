import time
from shogi_d.position import Position
from app import app
from context_d.client_socket import ClientSocket
from my_dynamodb.e_gov_bestmove import get_bestmove


class Context():
    def __init__(self):
        self._user_name = ''
        self._password = ''
        self._game_id = ''
        self._my_turn = ''
        self._current_turn = ''
        self._player_names = ['', '', '']
        # 局面
        self._position = Position()

        self._client_socket = ClientSocket()

        def none_func():
            pass

        # アグリーを返すコールバック関数
        self._agree_func = none_func

        def __go_func():
            """指し手を返すコールバック関数"""

            # a. 手番が回ってきた直後の待ち時間
            init_sec = 20  # 10, 20
            # b. 投票が無かったときの追加の待ち時間
            interval_sec = 10  # 5, 10
            # c. 投票を待つ回数
            tryal_max = 34  # 70, 34
            # サンプル
            #  a,  b,  c なら、 c*b +  a
            # 10,  5, 70 なら、70*5 + 10 = 360 = 6分
            # 20, 10, 34 なら、34*10 +20 = 360 = 6分

            # 手番が回ってきた直後の待ち時間
            time.sleep(init_sec)

            tryal_count = 0
            while True:
                m = get_bestmove()

                if not(m is None):
                    # 投票が溜まってたので指します
                    app.log.write_by_internal(
                        f"投票が溜まってたので指します [{m}]")
                    return m

                if tryal_max < tryal_count:
                    # 投了しよ
                    app.log.write_by_internal(
                        f"投票が無いので投了しよ tryal_count = [{m}]")
                    return '%TORYO'

                # 投票が無かったときの追加の待ち時間
                time.sleep(interval_sec)
                tryal_count += 1

        self._go_func = __go_func

    @property
    def client_socket(self):
        """通信ソケット"""
        return self._client_socket

    @client_socket.setter
    def client_socket(self, val):
        self._client_socket = val

    @property
    def user_name(self):
        """ログインユーザー名"""
        return self._user_name

    @user_name.setter
    def user_name(self, val):
        self._user_name = val

    @property
    def password(self):
        """パスワード"""
        return self._password

    @password.setter
    def password(self, val):
        self._password = val

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

    @property
    def player_names(self):
        """プレイヤー名 [未使用, 先手プレイヤー名, 後手プレイヤー名]"""
        return self._player_names

    @player_names.setter
    def player_names(self, val):
        self._player_names = val

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, val):
        self._position = val

    @property
    def agree_func(self):
        """アグリーを返すコールバック関数"""
        return self._agree_func

    @agree_func.setter
    def agree_func(self, func):
        self._agree_func = func

    @property
    def go_func(self):
        """指し手を返すコールバック関数"""
        return self._go_func

    @go_func.setter
    def go_func(self, func):
        self._go_func = func
