import sys
import signal
from app import app
from main import MainDiagram
from context import Context
from main_diagram import SplitTextBlock


class Test():
    def __init__(self):
        self._diagram = None

    @property
    def diagram(self):
        return self._diagram

    def set_up(self):
        context = Context()

        self._diagram = MainDiagram(context)

        # Implement test handlers
        def test_agree_func():
            """AGREE を送ると、 START: が返ってくるというシナリオ"""
            received = 'START:wdoor+floodgate-300-10F+e-gov-vote-kifuwarabe+Kristallweizen-Core2Duo-P7450+20211105220005'
            next_state_name, transition_key = self._diagram.state_machine.leave(
                received)
            app.log.write_by_internal(
                f"[DEBUG] Transition {transition_key} {next_state_name} (test.py 26 test_agree_func)")

            self._diagram.state_machine.arrive_sequence(next_state_name)

        # 後付け
        context.agree_func = test_agree_func

        def test_go_func():
            app.log.write_by_internal(
                f"[IN-TEST] go_func 投票を集めると料金かかるのでパス (test.py 34 test_go_func)")
            pass

        context.go_func = test_go_func

    def clean_up(self):
        self._diagram.clean_up()

    def run(self):
        """
        client-chat-3.log.txt 参照
        """

        # Send `LOGIN e-gov-vote-kifuwarabe floodgate-300-10F,egov-kif`

        received = 'LOGIN:e-gov-vote-kifuwarabe OK'
        next_state_name, transition_key = self._diagram.state_machine.leave(
            received)
        app.log.write_by_internal(
            f"[DEBUG] Transition {transition_key} {next_state_name} (test.py 46)")

        self._diagram.state_machine.arrive_sequence(next_state_name)
        if self._diagram.state_machine.state.name != '[Lobby]':
            app.log.write_by_internal('Unimplemented login')

        received = """BEGIN Game_Summary
Protocol_Version:1.2
Protocol_Mode:Server
Format:Shogi 1.0
Declaration:Jishogi 1.1
Game_ID:wdoor+floodgate-300-10F+e-gov-vote-kifuwarabe+Kristallweizen-Core2Duo-P7450+20211105220005
Name+:e-gov-vote-kifuwarabe
Name-:Kristallweizen-Core2Duo-P7450
Your_Turn:+
Rematch_On_Draw:NO
To_Move:+
Max_Moves:256
BEGIN Time
Time_Unit:1sec
Total_Time:300
Byoyomi:0
Increment:10
Least_Time_Per_Move:0
END Time
BEGIN Position
P1-KY-KE-GI-KI-OU-KI-GI-KE-KY
P2 * -HI *  *  *  *  * -KA * 
P3-FU-FU-FU-FU-FU-FU-FU-FU-FU
P4 *  *  *  *  *  *  *  *  * 
P5 *  *  *  *  *  *  *  *  * 
P6 *  *  *  *  *  *  *  *  * 
P7+FU+FU+FU+FU+FU+FU+FU+FU+FU
P8 * +KA *  *  *  *  * +HI * 
P9+KY+KE+GI+KI+OU+KI+GI+KE+KY
+
END Position
END Game_Summary
"""

        lines = SplitTextBlock(received)

        for line in lines:
            app.log.write_by_internal(
                f"[DEBUG] state=[{self._diagram.state_machine.state.name}] line=[{line}]")
            next_state_name, transition_key = self._diagram.state_machine.leave(
                line)
            app.log.write_by_internal(
                f"[DEBUG] Transition {transition_key} {next_state_name} (test.py 94)")

            self._diagram.state_machine.arrive_sequence(next_state_name)

        if self._diagram.state_machine.state.name != '[Reply]':
            app.log.write_by_internal(
                f'(Err.100) Unexpected state_name=[{self._diagram.state_machine.state.name}]')

        text = self._diagram.state_machine.context.position.formatBoard()
        app.log.write_by_internal(text)

        # 自分が先手か後手か
        app.log.write_by_internal(
            f"[DEBUG] my_turn=[{self._diagram.state_machine.context.my_turn}]")
        app.log.write_by_internal(
            f"[DEBUG] current_turn=[{self._diagram.state_machine.context.current_turn}]")

        if self._diagram.state_machine.context.my_turn != self._diagram.state_machine.context.current_turn:
            app.log.write_by_internal(f"[ERROR] 手番が違う")
            return

        app.log.write_by_internal(f"[DEBUG] わたしのターン。`+5756FU` を送信したとして")
        received = '+5756FU,T20'
        next_state_name, transition_key = self._diagram.state_machine.leave(
            received)
        app.log.write_by_internal(
            f"[DEBUG] Transition {transition_key} {next_state_name} (test.py 120)")

        self._diagram.state_machine.arrive_sequence(next_state_name)
        text = self._diagram.state_machine.context.position.formatBoard()
        app.log.write_by_internal(text)

        # 相手が指したとして
        received = '-3334FU,T35'
        next_state_name, transition_key = self._diagram.state_machine.leave(
            received)
        app.log.write_by_internal(
            f"[DEBUG] Transition {transition_key} {next_state_name} (test.py 131)")

        self._diagram.state_machine.arrive_sequence(next_state_name)
        text = self._diagram.state_machine.context.position.formatBoard()
        app.log.write_by_internal(text)


def test():
    def sigterm_handler(_signum, _frame) -> None:
        sys.exit(1)

    # 強制終了のシグナルを受け取ったら、強制終了するようにします
    signal.signal(signal.SIGTERM, sigterm_handler)

    test = Test()
    test.set_up()

    try:
        test.run()

    finally:
        # 強制終了のシグナルを無視するようにしてから、クリーンアップ処理へ進みます
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        test.clean_up()
        # 強制終了のシグナルを有効に戻します
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        signal.signal(signal.SIGINT, signal.SIG_DFL)


# Test
# python.exe -m test
if __name__ == "__main__":
    """テストします"""
    sys.exit(test())
