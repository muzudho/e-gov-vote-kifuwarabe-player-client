import re
from app import app
from state_machine_d.abstract_state import AbstractState
from context import Context


class AgreementState(AbstractState):
    def __init__(self):
        super().__init__()

        # [START:wdoor+floodgate-300-10F+e-gov-vote-kifuwarabe+Kristallweizen-Core2Duo-P7450+20211105220005]
        #        ------------------------------------------------------------------------------------------
        #        1. game_id
        self._start_pattern = re.compile(r'^START:([0-9A-Za-z_+-]+)$')

        def none_func(context):
            return '----Unimplemented---->'

        # ----Start----> 時のコールバック関数
        self._on_start = none_func

    @property
    def name(self):
        return "[Agreement]"

    @property
    def on_start(self):
        """----Start----> 時のコールバック関数"""
        return self._on_start

    @on_start.setter
    def on_start(self, func):
        self._on_start = func

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
                self.on_start(context)
                return '----Start---->'
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
    state = AgreementState()

    line = 'START:wdoor+floodgate-300-10F+e-gov-vote-kifuwarabe+Kristallweizen-Core2Duo-P7450+20211105220005'
    edge_name = state.leave(context, line)
    if edge_name == '----Start---->':
        app.log.write_by_internal('.', end='')
    else:
        app.log.write_by_internal('f', end='')
