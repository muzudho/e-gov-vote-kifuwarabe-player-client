import re


class NoneState():
    def __init__(self):
        # Format: `LOGIN:<username> OK`
        # Example: `LOGIN:e-gov-vote-kifuwarabe OK`
        self._login_ok_pattern = re.compile(
            r'^LOGIN:([0-9A-Za-z_-]{1,32}) OK$')

        self._user_name = ''

    @property
    def name(self):
        return "<NoneState/>"

    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, val):
        self._user_name = val

    def parse_line(self, line):
        matched = self._login_ok_pattern.match(line)
        if matched:
            # ログイン成功
            self._user_name = matched.group(1)
            return '<NoneState.LoginOk/>'

        return '<NoneState.Unknown>'


# Test
# python.exe "./scripts/client_state/none_state.py"
if __name__ == "__main__":
    line = 'LOGIN:egov-kifuwarabe OK'

    none_state = NoneState()
    result = none_state.parse_line(line)
    if result == '<NoneState.LoginOk/>':
        print('.', end='')
    else:
        print('f', end='')
