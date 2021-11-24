import re


class LoginChoice():
    def __init__(self):
        # [LOGIN:e-gov-vote-kifuwarabe OK]
        #        ---------------------
        #        1. username
        self._login_ok_pattern = re.compile(
            r'^LOGIN:([0-9A-Za-z_-]{1,32}) OK$')

        self._user_name = ''

    @property
    def name(self):
        return "[Border]<Login>"

    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, val):
        self._user_name = val

    def forward(self, line):
        """状態遷移します
        Parameters
        ----------
        str : line
            入力文字列

        Returns
        -------
        str
            辺の名前
        """

        # ----[LOGIN:e-gov-vote-kifuwarabe OK]----> ログイン成功
        #            ---------------------
        #            1. username
        matched = self._login_ok_pattern.match(line)
        if matched:
            self._user_name = matched.group(1)
            return '--Ok--'

        return '--Fail--'


# Test
# python.exe "./scripts/border_state.py"
if __name__ == "__main__":
    line = 'LOGIN:egov-kifuwarabe OK'

    login_choice = LoginChoice()
    edge = login_choice.forward(line)
    if edge == '--Ok--':
        print('.', end='')
    else:
        print('f', end='')
