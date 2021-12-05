import re
from app import app
from floodgate.keywords import E_FLOODGATE, E_GAME_OVER, E_MOVE_C, E_MOVE_S, E_WCSC, JUDGEMENT
from shogi_d.csa_helper import do_move
from state_machine_py.abstract_state import AbstractState
from context import Context


class JudgementState(AbstractState):
    """`START:` してからの状態"""

    def __init__(self):
        super().__init__()

        # [+5756FU,T20]
        #  -            先後(+)(-)
        #   --          元升
        #     --        先升
        #       --      駒
        #          ---  消費時間（秒）
        self._move_pattern = re.compile(
            r"^([+-])(\d{2})(\d{2})(\w{2}),T(\d+)$")

    @property
    def name(self):
        return JUDGEMENT

    def entry(self, req):
        super().entry(req)

        edge_path = ".".join(req.edge_path)

        if edge_path == "":
            pass
        elif edge_path == f"{E_MOVE_C}":
            pass
        elif edge_path == f"{E_MOVE_S}":
            pass
        elif edge_path == f"{E_GAME_OVER}":
            pass
        elif edge_path == f"{E_GAME_OVER}.{E_FLOODGATE}":
            pass
        elif edge_path == f"{E_GAME_OVER}.{E_WCSC}":
            pass
        else:
            raise ValueError(f"Edge path {edge_path} is not found")

        return None

    def exit(self, req):
        """次の辺の名前を返します

        Parameters
        ----------
        req : Request
            ステートマシンからステートへ与えられる引数のまとまり

        Returns
        -------
        str
            辺の名前
        """

        # ----[+5756FU,T20]---->
        #      -            先後(+)(-)
        #       --          元升
        #         --        先升
        #           --      駒
        #              ---  消費時間（秒）
        result = self._move_pattern.match(line)
        if result:
            phase = result.group(1)
            source = int(result.group(2))
            destination = int(result.group(3))
            piece = result.group(4)
            expend_time = int(result.group(5))

            do_move(context.position, phase, source,
                    destination, piece, expend_time)

            # 自分の指し手のエコーか、相手の指し手の通知か区別します
            if context.current_turn != context.my_turn:
                # 相手の指し手の通知だった
                self.on_play_me(context)
                return '----PlayMe---->'
            else:
                # 自分の指し手のエコーだった
                self.on_echo_self(context)
                return '----EchoSelf---->'

        # ----[#SENNICHITE]---->
        #      -----------
        #      千日手
        if line == '#SENNICHITE':
            self.on_sennichite(context)
            return '----Loopback---->'

        # ----[#OUTE_SENNICHITE]---->
        #      ----------------
        #      王手千日手
        if line == '#OUTE_SENNICHITE':
            self.on_oute_sennichite(context)
            return '----Loopback---->'

        # ----[#ILLEGAL_MOVE]---->
        #      -------------
        #      非合法手
        if line == '#ILLEGAL_MOVE':
            self.on_illegal_move(context)
            return '----Loopback---->'

        # ----[#TIME_UP]---->
        #      --------
        #      時間切れ
        if line == '#TIME_UP':
            self.on_time_up(context)
            return '----Loopback---->'

        # ----[#RESIGN]---->
        #      -------
        #      投了
        if line == '#RESIGN':
            self.on_resign(context)
            return '----Loopback---->'

        # ----[#JISHOGI]---->
        #      --------
        #      持将棋
        if line == '#JISHOGI':
            self.on_jishogi(context)
            return '----Loopback---->'

        # ----[#ILLEGAL_ACTION]---->
        #      ---------------
        #      相手の手番で指したなど
        if line == '#ILLEGAL_ACTION':
            self.on_illegal_action(context)
            return '----Loopback---->'

        # ----[#WIN]---->
        #      ----
        #      勝ち
        if line == '#WIN':
            self.on_win(context)
            return '----Win---->'

        # ----[#LOSE]---->
        #      -----
        #      負け
        if line == '#LOSE':
            self.on_lose(context)
            return '----Lose---->'

        # ----[#CENSORED]---->
        #      ---------
        #      手数上限に達して勝敗が付かなかった時
        if line == '#CENSORED':
            self.on_censored(context)
            return '----Lose---->'

        # ----[??????]---->
        #      ------
        #      その他
        return '----Unknown1---->'

    def on_move_c(self, req):
        pass

    def on_move_s(self, req):
        pass

    def on_game_over(self, req):
        pass

    def on_floodgate(self, req):
        pass

    def on_wcsc(self, req):
        pass

    def on_sennichite(self, context):
        """千日手の時"""
        pass

    def on_oute_sennichite(self, context):
        """王手千日手の時"""
        pass

    def on_illegal_move(self, context):
        """----IllegalMove---->時"""
        pass

    def on_time_up(self, context):
        """----TimeUp---->時"""
        pass

    def on_resign(self, context):
        """投了時"""
        pass

    def on_jishogi(self, context):
        """持将棋"""
        pass

    def on_illegal_action(self, context):
        """相手の手番で指したなど"""
        pass

    def on_win(self, context):
        """----Win---->時"""
        pass

    def on_lose(self, context):
        """----Lose---->時"""
        pass

    def on_censored(self, context):
        """手数上限に達して勝敗が付かなかった時"""
        pass


# Test
# python.exe -m floodgate_client_state.state_d.judgement
if __name__ == "__main__":
    app.log.set_up()
    context = Context()
    state = JudgementState()

    line = '+5756FU,T20'
    edge_name = state.leave(context, line)
    if edge_name == '----EchoSelf---->':
        app.log.write_by_internal('.', end='')
    else:
        app.log.write_by_internal('f', end='')
