import re
from state_machine_py.abstract_state import AbstractState
from app import app
from context import Context


class ReplyState(AbstractState):
    def __init__(self):
        super().__init__()

        # [START:wdoor+floodgate-300-10F+e-gov-vote-kifuwarabe+Kristallweizen-Core2Duo-P7450+20211105220005]
        #        ------------------------------------------------------------------------------------------
        #        1. game_id
        self._start_pattern = re.compile(r'^START:([0-9A-Za-z_+-]+)$')

    @property
    def name(self):
        return "[Reply]"

    def on_start_me(self, context):
        pass

    def on_start_you(self, context):
        pass

    def leave(self, context, line):
        """次の辺の名前を返します
        Parameters
        ----------
        str : line
            文字列（末尾に改行なし）

        Returns
        -------
        str
            辺の名前
        """
        pass

        # ----[START:wdoor+floodgate-300-10F+e-gov-vote-kifuwarabe+Kristallweizen-Core2Duo-P7450+20211105220005]----> 対局合意成立
        #            ------------------------------------------------------------------------------------------
        #            1. game_id
        matched = self._start_pattern.match(line)
        if matched:
            start_game_id = matched.group(1)
            if context.game_id == start_game_id:

                # TODO 自分の手番か、相手の手番かで分けたい
                if context.my_turn == context.current_turn:
                    # 初手を考えます
                    self.on_start_me(context)
                    return '----StartMe---->'
                else:
                    self.on_start_you(context)
                    return '----StartOpponent---->'

            else:
                raise ValueError(
                    f'GameIdが一致しませんでした context.game_id:{context.game_id} Start:{start_game_id}')

        app.log.write_by_internal(
            f"[DEBUG] Unknown line=[{line}]")
        return '----Loopback---->'


# Test
# python.exe -m floodgate_client.state_d.agreement
if __name__ == "__main__":
    app.log.set_up()
    context = Context()
    context.game_id = 'wdoor+floodgate-300-10F+e-gov-vote-kifuwarabe+Kristallweizen-Core2Duo-P7450+20211105220005'
    state = ReplyState()

    line = 'START:wdoor+floodgate-300-10F+e-gov-vote-kifuwarabe+Kristallweizen-Core2Duo-P7450+20211105220005'
    edge_name = state.leave(context, line)
    if edge_name == '----Start---->':
        app.log.write_by_internal('.', end='')
    else:
        app.log.write_by_internal('f', end='')
