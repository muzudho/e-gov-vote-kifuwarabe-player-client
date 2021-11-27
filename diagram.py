import time
from app import app
from state_machine_d.state_machine import StateMachine
from floodgate_client.context import Context
from floodgate_client.transition_dict import transition_dict
from floodgate_client.game_over_state_impl import GameOverStateImpl
from my_dynamodb.e_gov_bestmove import get_bestmove
from floodgate_client.none_state_impl import create_none_state
from floodgate_client.game_summary_state_impl import GameSummaryStateImpl
from floodgate_client.agreement_state_impl import AgreementStateImpl
from floodgate_client.game_state_impl import GameStateImpl
from floodgate_client.state_creator_dict import state_creator_dict


class Diagram():
    def __init__(self):

        self._state_machine = StateMachine(
            context=Context(), state_creator_dict=state_creator_dict, transition_dict=transition_dict)

        def none_func():
            pass

        # アグリーを返すコールバック関数
        self._agree_func = none_func

        # 指し手を返すコールバック関数
        def go_func():

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

        self._go_func = go_func

    @property
    def state_machine(self):
        """ダイアグラム"""
        return self._state_machine

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
