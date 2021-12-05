from floodgate.keywords import E_AGREE, E_COMPLETED, E_FLOODGATE, E_GAME_OVER, E_GAME_SUMMARY, E_INCORRECT, E_LOGIN, E_LOGOUT, E_MOVE, E_MOVE_ECHO, E_OK, E_REJECT, E_START, E_WCSC, GAME, INIT, LOBBY, REPLY

# Client side
transition_dict = {
    INIT: {
        E_LOGIN: {
            E_INCORRECT: INIT,
            E_OK: LOBBY,
        }
    },
    LOBBY: {
        E_LOGOUT: {
            E_COMPLETED: INIT
        },
        E_GAME_SUMMARY: REPLY
    },
    REPLY: {
        E_AGREE: {
            E_START: GAME
        },
        E_REJECT: {
            E_REJECT: LOBBY
        }
    },
    GAME: {
        E_MOVE: GAME,
        E_MOVE_ECHO: GAME,
        E_GAME_OVER: {
            E_FLOODGATE: INIT,
            E_WCSC: LOBBY,
        }
    },
}
