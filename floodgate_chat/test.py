import sys
import signal
from client import Client
from floodgate_chat.client_state_diagram_d.client_state_diagram import SplitTextBlock


class Test():
    def __init__(self):
        self._client = None

    @property
    def client(self):
        return self._client

    def set_up(self):
        self._client = Client()
        self._client.set_up()

        # Implement test handlers
        def __agree_func():
            """AGREE を送ると、 START: が返ってくるというシナリオ"""
            received = 'START:wdoor+floodgate-300-10F+e-gov-vote-kifuwarabe+Kristallweizen-Core2Duo-P7450+20211105220005'
            self._client.state_diagram.forward(received)

        self._client.state_diagram.agree_func = __agree_func

    def clean_up(self):
        self._client.clean_up()

    def run(self):
        """
        client-chat-3.log.txt 参照
        """

        # Send `LOGIN e-gov-vote-kifuwarabe floodgate-300-10F,egov-kif`

        received = 'LOGIN:e-gov-vote-kifuwarabe OK'
        self._client.state_diagram.forward(received)
        if self._client.state_diagram.state.name != '[LoggedIn]<LoggedIn>':
            print('Unimplemented login')

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
            print(
                f"[DEBUG] state=[{self._client.state_diagram.state.name}] line=[{line}]")
            self._client.state_diagram.forward(line)

        if self._client.state_diagram.state.name != '[Game]':
            print(
                f'Unimplemented begin board. client.state_diagram.state.name=[{self._client.state_diagram.state.name}]')

        text = self._client.state_diagram.state.position.formatBoard()
        print(text)

        # 自分が先手か後手か
        print(f"[DEBUG] my_turn=[{self._client.state_diagram.my_turn}]")
        print(
            f"[DEBUG] current_turn=[{self._client.state_diagram.current_turn}]")

        if self._client.state_diagram.my_turn != self._client.state_diagram.current_turn:
            print(f"[ERROR] 手番が違う")
            return

        print(f"[DEBUG] わたしのターン")
        # `+5756FU` を送信したとして
        received = '+5756FU,T20'
        self._client.state_diagram.forward(received)
        text = self._client.state_diagram.state.position.formatBoard()
        print(text)

        # 相手が指したとして
        received = '-3334FU,T35'
        self._client.state_diagram.forward(received)
        text = self._client.state_diagram.state.position.formatBoard()
        print(text)


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
# python.exe "./scripts/client_state_diagram.py"
if __name__ == "__main__":
    """テストします"""
    sys.exit(test())
