from floodgate.keywords import E_AGREE, E_COMPLETED, E_FLOODGATE, E_GAME_OVER, E_GAME_SUMMARY, E_INCORRECT, E_LOGIN, E_LOGOUT, E_MOVE, E_MOVE_ECHO, E_OK, E_REJECT, E_START, E_WCSC, GAME, INIT, JUDGEMENT, LOBBY, MATCH, RECEIPT, REPLY, TELL

# Server side
transition_dict = {
    RECEIPT: {
        E_LOGIN: {
            E_INCORRECT: RECEIPT,
            E_OK: MATCH,
        }
    },
    MATCH: {
        E_LOGOUT: {
            E_COMPLETED: RECEIPT
        },
        E_GAME_SUMMARY: TELL
    },
    TELL: {
        E_AGREE: {
            E_START: JUDGEMENT
        },
        E_REJECT: {
            E_REJECT: MATCH
        }
    },
    JUDGEMENT: {
        E_MOVE: JUDGEMENT,
        E_MOVE_ECHO: JUDGEMENT,
        E_GAME_OVER: {
            E_FLOODGATE: RECEIPT,
            E_WCSC: MATCH,
        }
    },
}
