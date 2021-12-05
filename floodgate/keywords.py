# GUI side state

INIT = "[Init]"
LOBBY = "[Lobby]"
REPLY = "[Reply]"
GAME = "[Game]"

# Server side state

RECEIPT = "[Receipt]"
MATCH = "[Match]"
TELL = "[Tell]"
JUDGEMENT = "[Judgement]"

# Edges 共通

E_FLOODGATE = "-Floodgate->"
E_WCSC = "-Wcsc->"
E_REJECT = "-Reject->"

# Edges Client side

E_LOGIN = "-Login->"
E_LOGOUT = "-Logout->"
E_AGREE = "-Agree->"
E_EMPTY = "-Empty->"
E_MOVE_C = "-MoveC->"

# Edges Server side

E_OK = "-Ok->"
E_INCORRECT = "-Incorrect->"
E_COMPLETED = "-Completed->"
E_GAME_SUMMARY = "-GameSummary->"
E_START = "-Start->"
E_GAME_OVER = "-GameOver->"
E_MOVE_S = "-MoveS->"
